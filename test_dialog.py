from modules.dialog import introduction, quiz, role_play

# Simule une session complète pour "Marie"
print("=== TEST INTRODUCTION ===")
introduction("Marie")          # doit lire la mémoire de Marie

print("\n=== TEST QUIZ ===")
quiz("Marie", 10)              # doit enregistrer le résultat

print("\n=== TEST DEUXIÈME SESSION ===")
introduction("Marie")          # doit maintenant afficher le message mémoire
