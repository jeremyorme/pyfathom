from pyfathom import *

in_strs = [
  '180g | 1 cup uncooked brown rice',
  '½ small butternut squash , cubed',
  '5½ tablespoons tahini (you can sub cashew butter)',
  'pecans 125g',
  'flat-leaf parsley a bunch, roughly chopped',
  'rocket 70g',
  'leftover marinade from the mushrooms',
  '15 oz (425 g) black beans, drained (reserve ¼ cup (60 ml) of the juice) and rinsed well',
  '1/4 teaspoon Garam Masala, for garnish',
  '2 tablespoons chopped cilantro, for garnish'
]

knowledge = '''
/pinch/ is unit
/mls?|mL|cc|millilitres?|milliliters?/ is unit
/tsps?|t|teaspoons?/ is unit
/tbsps?|Tbsps?|T|tbl|tbs|tablespoons?/ is unit
/floz/ is unit
/fl/,/oz/ is unit
/fluid/,/ounces?/ is unit
/p|pts?|pints?/ is unit
/ls?|L|litres?|liters?/ is unit
/gals?|gallons?/ is unit
/dls?|dL|decilitre|deciliter/ is unit
/gs?|grams?|grammes?/ is unit
/oz|ounces?/ is unit
/lbs?|#|pounds?/ is unit
/kgs?|kilos?|kilograms?/ is unit

/\d+/?,/\d+\/\d+/ is number
/\d+(\.\d+)?/ is number
/\d*[½⅓⅔¼¾⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞]/ is number
/a/ is number-word

number,/-|–/,number is range
/cups?/ is unit
range|number|number-word,/\-/?,unit?,/\./?,/of/? is amount
amount?,/plus/?,amount?,/[a-zA-Z\-]+/+,amount? is ,,,ingredient,
'''

cls = classifier(knowledge)
for in_str in in_strs:
  print(cls.classify(in_str))

