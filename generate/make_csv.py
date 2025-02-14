# functions used to create parameter_sets.csv

import itertools

variants = {"RSDP", "RSDPG"}

categories = {128: 1,
              192: 3,
              256: 5}

targets = {"small": "SIG_SIZE",
           "balanced": "BALANCED",
           "fast": "SPEED"}

implementations = {"clean", "avx2"}

def generate_namespace(variant, category, target, implementation):
  return f"PQCLEAN_CROSS{variant}{category}{target}_{implementation}_".upper()

def generate_dir_name(variant, category, target, implementation):
  return f"/cross-{variant}-{category}-{target}/{implementation}".lower()

combinations = itertools.product(variants, categories, targets, implementations)
for v,c,t,i in combinations:
  print(generate_dir_name(v,c,t,i))
  print(generate_namespace(v,c,t,i))

