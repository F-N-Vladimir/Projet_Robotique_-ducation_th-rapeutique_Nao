from modules.memory import MemoryModule

# Test 1 : première visite
mem = MemoryModule("Lucas")
print("=== PREMIÈRE VISITE ===")
print(mem.get_message_accueil())

# Test 2 : enregistrer une session avec une erreur
mem.enregistrer_session(
    theme="hypoglycemie",
    score=0,
    total=1,
    erreurs_themes=["hypoglycemie"]
)
print("\n=== APRÈS SESSION 1 ===")
print("Stats :", mem.get_stats_dict())

# Test 3 : simuler une deuxième visite
mem2 = MemoryModule("Lucas")
print("\n=== DEUXIÈME VISITE ===")
print(mem2.get_message_accueil())
