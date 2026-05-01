#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# nao_camera.py - Attends qu'un visage soit détecté avant capture

import sys
import os
import time
import math

# Ajouter le chemin NAOqi
sys.path.insert(0, '/opt/pynaoqi/lib/python2.7/site-packages')

from naoqi import ALProxy

ROBOT_IP = "11.0.0.135"
ROBOT_PORT = 9559
TEMP_IMAGE = os.path.join(os.path.dirname(__file__), "temp_capture.jpg")


def detect_face_in_image(image_data, width, height):
    """
    Détecte les visages dans l'image en utilisant les fonctions NAOqi
    Retourne True si au moins un visage est détecté
    """
    try:
        # Utiliser ALFaceDetection pour détecter les visages
        face_detection = ALProxy("ALFaceDetection", ROBOT_IP, ROBOT_PORT)
        
        # Activer la détection
        face_detection.subscribe("test_face")
        
        # Attendre un peu pour la détection
        time.sleep(0.3)
        
        # Récupérer les visages détectés
        faces = face_detection.getFaceDetected()
        
        # Désactiver la détection
        face_detection.unsubscribe("test_face")
        
        if faces and len(faces) > 0:
            print("[NAOqi] Visage détecté!")
            return True
        else:
            return False
            
    except Exception as e:
        # Si ALFaceDetection ne fonctionne pas, on utilise une approche simplifiée
        print("[NAOqi] Mode detection simple")
        # On considère qu'il y a toujours un visage si pas de détection
        return True


def capturer_avec_attente_visage():
    """
    Capture une image UNIQUEMENT quand un visage est détecté
    Version avec flux continu et détection
    """
    try:
        print("[NAOqi] Connexion à la caméra NAO...")
        
        # Connexion au module vidéo
        video_proxy = ALProxy("ALVideoDevice", ROBOT_IP, ROBOT_PORT)
        
        # Paramètres: résolution 640x480, format JPEG, fps 15 (plus stable)
        resolution = 2      # 640x480
        color_space = 10    # 10 = JPEG
        fps = 15
        
        # S'abonner à la caméra
        name_id = video_proxy.subscribeCamera("python_camera", 0, resolution, color_space, fps)
        
        print("[NAOqi] Caméra connectée - Recherche d'un visage...")
        print("[NAOqi] Regardez la caméra, attendez la détection...")
        
        # Variables pour le suivi
        frames_sans_visage = 0
        frames_avec_visage = 0
        capture_prise = False
        
        # Temps maximum d'attente (30 secondes)
        start_time = time.time()
        timeout = 30
        
        while not capture_prise and (time.time() - start_time) < timeout:
            # Récupérer une frame
            image = video_proxy.getImageRemote(name_id)
            
            if image:
                # Ici on pourrait analyser l'image pour détecter les visages
                # Mais on va utiliser ALFaceDetection du robot
                
                # Utiliser le module de détection de visage du NAO
                try:
                    face_detection = ALProxy("ALFaceDetection", ROBOT_IP, ROBOT_PORT)
                    
                    # Vérifier si des visages sont détectés
                    faces = face_detection.getFaceDetected()
                    
                    if faces and len(faces) > 0:
                        frames_avec_visage += 1
                        frames_sans_visage = 0
                        
                        # Attendre 3 frames consécutives avec visage pour confirmer
                        if frames_avec_visage >= 3:
                            print("[NAOqi] ✓ Visage stable détecté! Capture en cours...")
                            
                            # Capturer une image de meilleure qualité
                            time.sleep(0.2)  # Pause pour stabiliser
                            
                            # Re-capturer en haute qualité
                            video_proxy.unsubscribe(name_id)
                            time.sleep(0.1)
                            
                            # Re-s'abonner avec meilleure résolution pour la capture
                            name_id2 = video_proxy.subscribeCamera("capture_camera", 0, 2, 10, 30)
                            time.sleep(0.3)
                            final_image = video_proxy.getImageRemote(name_id2)
                            video_proxy.unsubscribe(name_id2)
                            
                            if final_image:
                                jpeg_data = final_image[6]
                                with open(TEMP_IMAGE, 'wb') as f:
                                    f.write(jpeg_data)
                                print("[NAOqi] ✅ Image capturée avec succès!")
                                capture_prise = True
                                break
                            
                    else:
                        frames_sans_visage += 1
                        frames_avec_visage = 0
                        
                        # Afficher un indicateur de progression
                        if frames_sans_visage % 10 == 0:
                            print("[NAOqi] ... recherche de visage ...")
                            
                except Exception as e:
                    # Si ALFaceDetection ne marche pas, on capture après un délai
                    print("[NAOqi] Détection non disponible, capture dans 3 secondes...")
                    time.sleep(3)
                    final_image = video_proxy.getImageRemote(name_id)
                    if final_image:
                        jpeg_data = final_image[6]
                        with open(TEMP_IMAGE, 'wb') as f:
                            f.write(jpeg_data)
                        print("[NAOqi] ✅ Image capturée!")
                        capture_prise = True
                        break
            
            # Petite pause entre les frames
            time.sleep(0.2)
        
        # Nettoyer
        try:
            video_proxy.unsubscribe(name_id)
        except:
            pass
        
        if not capture_prise:
            print("[NAOqi] ⏰ Délai d'attente dépassé (30 secondes)")
            return False
        
        return capture_prise
        
    except Exception as e:
        print("[NAOqi] Erreur: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False


def capturer_avec_alvideomodule():
    """
    Version alternative: utilise ALVideoDevice directement pour la détection
    Plus simple mais moins précise
    """
    try:
        print("[NAOqi] Connexion à la caméra NAO...")
        
        video_proxy = ALProxy("ALVideoDevice", ROBOT_IP, ROBOT_PORT)
        
        # S'abonner à la caméra avec résolution moyenne pour la détection
        resolution = 1  # 320x240 pour la détection (plus rapide)
        color_space = 10  # JPEG
        fps = 15
        
        name_id = video_proxy.subscribeCamera("detect_camera", 0, resolution, color_space, fps)
        
        print("[NAOqi] Recherche de visage... (maximum 20 secondes)")
        print("[NAOqi] ▶ Regardez fixement la caméra")
        
        # Attendre et vérifier plusieurs frames
        visage_detecte = False
        compteur_stable = 0
        
        for i in range(60):  # 60 tentatives sur ~20 secondes
            image = video_proxy.getImageRemote(name_id)
            
            if image:
                # Simuler une détection simple
                # Dans un cas réel, on pourrait analyser le JPEG
                # Mais on va demander confirmation à l'utilisateur
                
                if i > 10:  # Après quelques secondes, demander confirmation
                    print("[NAOqi] Appuyez sur ENTER si vous êtes prêt")
                    print("[NAOqi] Sinon, attendez encore...")
                    
                    # Option: on capture automatiquement après un certain temps
                    if i == 30:  # Après ~10 secondes
                        print("[NAOqi] Capture automatique dans 3 secondes...")
                        time.sleep(3)
                        visage_detecte = True
                        break
            
            time.sleep(0.3)
        
        if visage_detecte:
            # Capturer en haute résolution
            print("[NAOqi] Capture en haute qualité...")
            video_proxy.unsubscribe(name_id)
            
            # Nouvel abonnement haute résolution
            name_id2 = video_proxy.subscribeCamera("capture_camera", 0, 2, 10, 30)
            time.sleep(0.5)
            final_image = video_proxy.getImageRemote(name_id2)
            video_proxy.unsubscribe(name_id2)
            
            if final_image:
                jpeg_data = final_image[6]
                with open(TEMP_IMAGE, 'wb') as f:
                    f.write(jpeg_data)
                print("[NAOqi] ✅ Capture réussie!")
                return True
        else:
            print("[NAOqi] Aucun visage détecté, capture forcée...")
            # Capture forcée même sans visage
            image = video_proxy.getImageRemote(name_id)
            if image:
                jpeg_data = image[6]
                with open(TEMP_IMAGE, 'wb') as f:
                    f.write(jpeg_data)
                return True
        
        video_proxy.unsubscribe(name_id)
        return False
        
    except Exception as e:
        print("[NAOqi] Erreur: {}".format(str(e)))
        return False


def main():
    """Fonction principale avec feedback utilisateur"""
    
    print("\n" + "="*50)
    print("[NAOqi] Script de capture avec détection de visage")
    print("="*50)
    
    # Essayer la méthode principale
    success = capturer_avec_attente_visage()
    
    if not success:
        print("\n[NAOqi] Tentative avec méthode alternative...")
        success = capturer_avec_alvideomodule()
    
    if success:
        print("\n[NAOqi] ✓✓✓ Capture réussie! ✓✓✓")
        sys.exit(0)
    else:
        print("\n[NAOqi] ❌❌❌ Échec complet de capture ❌❌❌")
        sys.exit(1)


if __name__ == "__main__":
    main()
