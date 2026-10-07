"""
Multilingual Idiom Dictionary and Knowledge Base
Supports: English (en), Hindi (hi), and Marathi (mr)

Contains canonical idiom metadata:
- canonical_concept: cross-lingual semantic concept identifier
- language: ISO 639-1 language code ('en', 'hi', 'mr')
- phrase: canonical expression
- aliases: inflectional variants, tenses, surface realizations
- meaning: figurative definition
- example: representative natural sentence
- category: thematic semantic classification
- idiomatic_keywords: figurative contextual cues
- literal_keywords: concrete / physical domain cues
- usage_notes: origin, register, and cultural context
"""

import unicodedata

# ══════════════════════════════════════════════════════════════════════════════
# MULTILINGUAL IDIOM KNOWLEDGE BASE (108 CANONICAL IDIOMS)
# ══════════════════════════════════════════════════════════════════════════════

IDIOM_DICTIONARY = {
    # ──────────────────────────────────────────────────────────────────────────
    # ENGLISH IDIOMS (36 CANONICAL EXPRESSIONS)
    # ──────────────────────────────────────────────────────────────────────────
    "break the ice": {
        "canonical_concept": "initiate_social_conversation",
        "language": "en",
        "phrase": "break the ice",
        "idiom": "break the ice",
        "aliases": ["break the ice", "broke the ice", "breaking the ice", "breaks the ice"],
        "meaning": "To initiate a social conversation or relieve tension in an awkward or formal situation.",
        "example": "He told a funny joke at the start of the meeting to break the ice.",
        "category": "Communication & Social",
        "idiomatic_keywords": ["conversation", "meeting", "awkward", "joke", "tension", "strangers", "party", "relax", "nervous", "introductory"],
        "literal_keywords": ["frozen", "freezer", "lake", "winter", "pick", "hammer", "glacier", "cold", "cube", "sculpture", "pond"],
        "usage_notes": "Commonly used in professional, social, and academic settings to describe easing social stiffness."
    },
    "piece of cake": {
        "canonical_concept": "effortless_task",
        "language": "en",
        "phrase": "piece of cake",
        "idiom": "piece of cake",
        "aliases": ["piece of cake", "pieces of cake"],
        "meaning": "Something that is very easy to accomplish or achieve.",
        "example": "The mathematics test was a piece of cake for the well-prepared student.",
        "category": "Difficulty & Effort",
        "idiomatic_keywords": ["easy", "simple", "exam", "test", "task", "effortless", "score", "breeze", "problem", "solve"],
        "literal_keywords": ["cake", "slice", "bakery", "eat", "dessert", "chocolate", "sweet", "fork", "plate", "icing", "baking"],
        "usage_notes": "Originated from cake-walk competitions where cake was awarded for easy accomplishments."
    },
    "once in a blue moon": {
        "canonical_concept": "extreme_rarity",
        "language": "en",
        "phrase": "once in a blue moon",
        "idiom": "once in a blue moon",
        "aliases": ["once in a blue moon", "in a blue moon"],
        "meaning": "An event or occurrence that happens very rarely or infrequently.",
        "example": "He travels abroad only once in a blue moon due to his busy schedule.",
        "category": "Time & Frequency",
        "idiomatic_keywords": ["rarely", "seldom", "infrequently", "hardly", "unusual", "occasion", "scarcely", "never"],
        "literal_keywords": ["moon", "astronomy", "lunar", "telescope", "sky", "orbit", "celestial", "night", "phase", "satellite"],
        "usage_notes": "Refers astronomically to the second full moon in a calendar month, which occurs approximately once every 2.7 years."
    },
    "hit the nail on the head": {
        "canonical_concept": "exact_accuracy",
        "language": "en",
        "phrase": "hit the nail on the head",
        "idiom": "hit the nail on the head",
        "aliases": ["hit the nail on the head", "hits the nail on the head", "hitting the nail on the head"],
        "meaning": "To describe exactly what is causing a situation or to state the precise truth.",
        "example": "Her analysis of the software bug hit the nail on the head.",
        "category": "Accuracy & Truth",
        "idiomatic_keywords": ["accurate", "precise", "correct", "analysis", "point", "identified", "truth", "diagnosis", "solution", "agreed"],
        "literal_keywords": ["hammer", "wood", "carpenter", "hardware", "tool", "strike", "plank", "construction", "steel"],
        "usage_notes": "Draws analogy from carpentry where driving a nail precisely on its center head delivers maximum efficiency."
    },
    "spill the beans": {
        "canonical_concept": "reveal_secret",
        "language": "en",
        "phrase": "spill the beans",
        "idiom": "spill the beans",
        "aliases": ["spill the beans", "spilled the beans", "spills the beans", "spilling the beans", "spilt the beans"],
        "meaning": "To disclose a secret or reveal confidential information prematurely.",
        "example": "He accidentally spilled the beans about the surprise anniversary celebration.",
        "category": "Secrets & Communication",
        "idiomatic_keywords": ["secret", "reveal", "confidential", "surprise", "disclose", "tell", "confessed", "spoiled", "plan", "truth"],
        "literal_keywords": ["beans", "kitchen", "jar", "cooking", "floor", "recipe", "legumes", "pot", "spilled", "dropped", "pantry"],
        "usage_notes": "Often linked to ancient voting rituals where colored beans were dropped into jars to cast secret ballots."
    },
    "under the weather": {
        "canonical_concept": "unwell_or_sick",
        "language": "en",
        "phrase": "under the weather",
        "idiom": "under the weather",
        "aliases": ["under the weather", "feeling under the weather", "felt under the weather"],
        "meaning": "Feeling slightly ill, unwell, indisposed, or fatigued.",
        "example": "After studying all night, Rahul was feeling under the weather.",
        "category": "Health & State",
        "idiomatic_keywords": ["sick", "unwell", "fever", "cold", "fatigue", "doctor", "health", "rest", "bed", "medicine", "headache", "studying"],
        "literal_keywords": ["weather", "forecast", "shelter", "climate", "rain", "storm", "umbrella", "meteorology", "outside", "temperature"],
        "usage_notes": "Maritime origin where sailors went below deck to protect themselves from adverse weather when feeling ill."
    },
    "cost an arm and a leg": {
        "canonical_concept": "exorbitant_cost",
        "language": "en",
        "phrase": "cost an arm and a leg",
        "idiom": "cost an arm and a leg",
        "aliases": ["cost an arm and a leg", "costs an arm and a leg", "costing an arm and a leg", "cost me an arm and a leg", "costs an arm and leg"],
        "meaning": "To be extremely expensive or exorbitantly priced.",
        "example": "The latest sports car costs an arm and a leg to maintain.",
        "category": "Cost & Value",
        "idiomatic_keywords": ["expensive", "price", "money", "cost", "luxury", "budget", "affordable", "bought", "dollars", "rupees", "overpriced"],
        "literal_keywords": ["limb", "amputation", "prosthetic", "body", "injury", "surgeon", "hospital", "anatomy", "physical"],
        "usage_notes": "Post-war figurative expression highlighting the immense sacrifice associated with acquiring something."
    },
    "bite the bullet": {
        "canonical_concept": "face_inevitable_hardship",
        "language": "en",
        "phrase": "bite the bullet",
        "idiom": "bite the bullet",
        "aliases": ["bite the bullet", "bit the bullet", "biting the bullet", "bites the bullet"],
        "meaning": "To face an inevitable grim situation with courage and fortitude.",
        "example": "He had to bite the bullet and accept the difficult pay cut during the company restructuring.",
        "category": "Decision & Courage",
        "idiomatic_keywords": ["courage", "face", "decision", "difficult", "inevitable", "confront", "endure", "accept", "restructuring", "challenge"],
        "literal_keywords": ["bullet", "gun", "ammunition", "rifle", "lead", "military", "shoot", "metal", "teeth", "biting"],
        "usage_notes": "Historical military practice of wounded soldiers biting lead bullets during battlefield surgery without anesthesia."
    },
    "let the cat out of the bag": {
        "canonical_concept": "inadvertent_disclosure",
        "language": "en",
        "phrase": "let the cat out of the bag",
        "idiom": "let the cat out of the bag",
        "aliases": ["let the cat out of the bag", "lets the cat out of the bag", "letting the cat out of the bag"],
        "meaning": "To inadvertently reveal a secret or confidential plan.",
        "example": "Sarah let the cat out of the bag regarding our upcoming product launch.",
        "category": "Secrets & Communication",
        "idiomatic_keywords": ["secret", "revealed", "confidential", "spoiled", "launch", "surprise", "hidden", "announced", "slip", "discovered"],
        "literal_keywords": ["cat", "bag", "feline", "pet", "kitten", "sack", "trapped", "animal", "carrier", "meow", "rescue"],
        "usage_notes": "Folklore connects this to market fraud where buyers purchased piglets in bags, only to find a cat swapped inside."
    },
    "beat around the bush": {
        "canonical_concept": "evade_direct_issue",
        "language": "en",
        "phrase": "beat around the bush",
        "idiom": "beat around the bush",
        "aliases": ["beat around the bush", "beats around the bush", "beating around the bush", "beat about the bush"],
        "meaning": "To discuss a matter without addressing the main point directly or purposefully evading it.",
        "example": "Stop beating around the bush and tell us the real reason for the delay.",
        "category": "Communication & Social",
        "idiomatic_keywords": ["direct", "point", "evading", "hesitant", "clear", "truth", "delay", "topic", "straightforward", "waffle"],
        "literal_keywords": ["bush", "hedge", "stick", "branches", "garden", "hunting", "birds", "foliage", "woods", "shrub"],
        "usage_notes": "Derived from traditional bird hunting where beaters drove game out by hitting surrounding foliage."
    },
    "blessing in disguise": {
        "canonical_concept": "misfortune_turns_good",
        "language": "en",
        "phrase": "blessing in disguise",
        "idiom": "blessing in disguise",
        "aliases": ["blessing in disguise", "blessings in disguise"],
        "meaning": "An apparent misfortune or negative event that eventually results in something unexpectedly positive.",
        "example": "Missing that flight was a blessing in disguise as it allowed him to attend the critical meeting.",
        "category": "Luck & Outcome",
        "idiomatic_keywords": ["fortune", "positive", "outcome", "unfortunate", "lucky", "advantage", "turned", "better", "opportunity"],
        "literal_keywords": ["mask", "costume", "disguise", "cloak", "prayer", "priest", "holy", "camouflage"],
        "usage_notes": "18th-century philosophical notion highlighting providential outcomes disguised behind temporary difficulties."
    },
    "burn the midnight oil": {
        "canonical_concept": "work_late_at_night",
        "language": "en",
        "phrase": "burn the midnight oil",
        "idiom": "burn the midnight oil",
        "aliases": ["burn the midnight oil", "burning the midnight oil", "burned the midnight oil", "burns the midnight oil"],
        "meaning": "To work or study late into the night.",
        "example": "The engineering team burned the midnight oil to submit the project before the deadline.",
        "category": "Effort & Work",
        "idiomatic_keywords": ["study", "work", "night", "deadline", "late", "exam", "project", "overtime", "effort", "tired"],
        "literal_keywords": ["lamp", "oil", "wick", "kerosene", "flame", "lantern", "fuel", "burning"],
        "usage_notes": "Refers to the era prior to electric lighting when scholars and artisans relied on oil lamps to work after dark."
    },
    "call it a day": {
        "canonical_concept": "cease_current_activity",
        "language": "en",
        "phrase": "call it a day",
        "idiom": "call it a day",
        "aliases": ["call it a day", "calling it a day", "called it a day", "calls it a day"],
        "meaning": "To stop working or discontinue an activity for the remainder of the day.",
        "example": "We have made good progress on the report, so let us call it a day.",
        "category": "Work & Rest",
        "idiomatic_keywords": ["stop", "finish", "rest", "conclude", "wrap", "tired", "evening", "work", "progress", "quit"],
        "literal_keywords": ["calendar", "hours", "sunrise", "sunset", "twenty-four", "daytime", "dawn", "dusk"],
        "usage_notes": "Originated from industrial employees referring to leaving work before the scheduled end of shift."
    },
    "on cloud nine": {
        "canonical_concept": "ecstatic_happiness",
        "language": "en",
        "phrase": "on cloud nine",
        "idiom": "on cloud nine",
        "aliases": ["on cloud nine", "on cloud 9", "upon cloud nine"],
        "meaning": "To experience a state of extreme euphoria, bliss, or happiness.",
        "example": "She was on cloud nine after receiving the university scholarship.",
        "category": "Emotion & Happiness",
        "idiomatic_keywords": ["happy", "ecstatic", "joy", "thrilled", "elated", "scholarship", "celebration", "excited", "bliss"],
        "literal_keywords": ["cumulonimbus", "cloud", "atmosphere", "sky", "altitude", "weather", "meteorology", "raincloud", "airplane"],
        "usage_notes": "Popularized by the 1896 International Cloud Atlas classification where Cloud Nine described soaring cumulonimbus clouds."
    },
    "pull someone's leg": {
        "canonical_concept": "tease_or_joke",
        "language": "en",
        "phrase": "pull someone's leg",
        "idiom": "pull someone's leg",
        "aliases": ["pull someone's leg", "pulling my leg", "pulled my leg", "pulling his leg", "pulled her leg", "pull your leg"],
        "meaning": "To tease or deceive someone humorously in a playful manner.",
        "example": "Do not take him seriously; he is just pulling your leg about winning the lottery.",
        "category": "Humor & Social",
        "idiomatic_keywords": ["joke", "tease", "kidding", "fool", "humor", "playful", "prank", "laugh", "serious", "deceive"],
        "literal_keywords": ["leg", "ankle", "muscle", "physical", "tug", "rope", "knee", "limb", "stretch"],
        "usage_notes": "Originally associated with 19th-century street ruffians who physically tripped pedestrians with wires to rob them."
    },
    "raining cats and dogs": {
        "canonical_concept": "heavy_downpour",
        "language": "en",
        "phrase": "raining cats and dogs",
        "idiom": "raining cats and dogs",
        "aliases": ["raining cats and dogs", "rained cats and dogs", "rains cats and dogs"],
        "meaning": "Raining exceptionally heavily or with intense torrential force.",
        "example": "We could not drive home because it was raining cats and dogs outside.",
        "category": "Weather & Nature",
        "idiomatic_keywords": ["rain", "storm", "downpour", "heavy", "flood", "torrential", "soaked", "monsoon", "thunder", "umbrella"],
        "literal_keywords": ["puppy", "kitten", "feline", "canine", "animal", "pets", "barking", "meowing", "falling"],
        "usage_notes": "Often traced to 17th-century England where severe urban downpours washed stray animals down overflowing drainage gutters."
    },
    "a dime a dozen": {
        "canonical_concept": "common_and_low_value",
        "language": "en",
        "phrase": "a dime a dozen",
        "idiom": "a dime a dozen",
        "aliases": ["a dime a dozen", "dime a dozen"],
        "meaning": "Very common, ubiquitous, and therefore having minimal intrinsic or distinguished value.",
        "example": "Cheap generic plastic gadgets are a dime a dozen at the local street fair.",
        "category": "Value & Abundance",
        "idiomatic_keywords": ["common", "cheap", "plentiful", "abundant", "ordinary", "generic", "worthless", "everywhere", "standard"],
        "literal_keywords": ["dime", "coin", "twelve", "dozen", "cents", "currency", "purchasing", "supermarket", "baker"],
        "usage_notes": "Refers to American grocery pricing in the late 1800s where 12 produce items cost merely a single 10-cent dime."
    },
    "kill two birds with one stone": {
        "canonical_concept": "dual_achievement",
        "language": "en",
        "phrase": "kill two birds with one stone",
        "idiom": "kill two birds with one stone",
        "aliases": ["kill two birds with one stone", "killed two birds with one stone", "killing two birds with one stone"],
        "meaning": "To accomplish two distinct objectives simultaneously through a single decisive action.",
        "example": "Cycling to work kills two birds with one stone by saving fuel money and providing daily exercise.",
        "category": "Efficiency & Strategy",
        "idiomatic_keywords": ["efficiency", "simultaneous", "action", "tasks", "solved", "single", "benefit", "multitasking", "productive"],
        "literal_keywords": ["slingshot", "stone", "pebble", "hunting", "birds", "feathers", "throw", "target", "weapon"],
        "usage_notes": "Ancient proverb found in various languages, symbolizing resourcefulness and precision hunting."
    },
    "barking up the wrong tree": {
        "canonical_concept": "pursuing_mistaken_course",
        "language": "en",
        "phrase": "barking up the wrong tree",
        "idiom": "barking up the wrong tree",
        "aliases": ["barking up the wrong tree", "barked up the wrong tree", "barks up the wrong tree"],
        "meaning": "Pursuing a mistaken line of thought or accusing the wrong individual.",
        "example": "If you suspect Marcus took the office keys, you are barking up the wrong tree.",
        "category": "Accuracy & Error",
        "idiomatic_keywords": ["mistaken", "wrong", "accusing", "misguided", "suspect", "clue", "direction", "investigation", "fault"],
        "literal_keywords": ["hound", "dog", "hunting", "tree", "branches", "bark", "raccoon", "forest", "canine", "trunk"],
        "usage_notes": "American hunting phrase where hunting dogs mistakenly barked at an empty tree while the quarry escaped elsewhere."
    },
    "elephant in the room": {
        "canonical_concept": "unaddressed_obvious_issue",
        "language": "en",
        "phrase": "elephant in the room",
        "idiom": "elephant in the room",
        "aliases": ["elephant in the room", "elephants in the room"],
        "meaning": "An obvious, major problem or controversial issue that everyone recognizes but avoids discussing.",
        "example": "The impending budget deficit was the elephant in the room that no director wanted to mention.",
        "category": "Social & Communication",
        "idiomatic_keywords": ["taboo", "ignore", "obvious", "unspoken", "tension", "avoiding", "awkward", "problem", "meeting", "silence"],
        "literal_keywords": ["pachyderm", "trunk", "tusks", "zoo", "safari", "animal", "living", "room", "walls", "furniture"],
        "usage_notes": "Recorded in English literature since the mid-20th century to convey an impossible-to-miss reality that is willfully ignored."
    },
    "best of both worlds": {
        "canonical_concept": "dual_advantages",
        "language": "en",
        "phrase": "best of both worlds",
        "idiom": "best of both worlds",
        "aliases": ["best of both worlds"],
        "meaning": "A favorable situation where one enjoys the benefits of two contradictory choices simultaneously.",
        "example": "Working remotely while retaining a city salary gives her the best of both worlds.",
        "category": "Advantage & Lifestyle",
        "idiomatic_keywords": ["benefit", "advantage", "ideal", "combination", "lifestyle", "flexibility", "perfect", "enjoy", "balance"],
        "literal_keywords": ["planets", "globes", "universe", "celestial", "dimension", "astronomy", "earth"],
        "usage_notes": "Used widely in modern sociology and economics to describe harmonious multi-benefit arrangements."
    },
    "add fuel to the fire": {
        "canonical_concept": "escalate_conflict",
        "language": "en",
        "phrase": "add fuel to the fire",
        "idiom": "add fuel to the fire",
        "aliases": ["add fuel to the fire", "added fuel to the fire", "adding fuel to the fire", "adds fuel to the fire"],
        "meaning": "To exacerbate an already intense conflict, argument, or precarious situation.",
        "example": "His sarcastic commentary only added fuel to the fire during the union debate.",
        "category": "Conflict & Escalation",
        "idiomatic_keywords": ["worse", "escalate", "anger", "conflict", "argument", "worsened", "provoke", "temper", "dispute"],
        "literal_keywords": ["gasoline", "wood", "logs", "flame", "bonfire", "campfire", "kerosene", "burning", "sparks"],
        "usage_notes": "Traced back to ancient Roman literature (Livy) describing the foolish act of feeding an active blaze."
    },
    "cut corners": {
        "canonical_concept": "sacrifice_quality_for_speed",
        "language": "en",
        "phrase": "cut corners",
        "idiom": "cut corners",
        "aliases": ["cut corners", "cutting corners", "cuts corners"],
        "meaning": "To execute a task poorly, cheaply, or carelessly to conserve time or financial expenditure.",
        "example": "The construction company cut corners on concrete reinforcement, causing safety hazards.",
        "category": "Quality & Ethics",
        "idiomatic_keywords": ["cheap", "quality", "careless", "safety", "standard", "rushed", "budget", "compromise", "flaws", "inspectors"],
        "literal_keywords": ["scissors", "paper", "angles", "sharp", "geometric", "turn", "street", "curb", "cutting", "rectangle"],
        "usage_notes": "19th-century driving terminology referring to drivers cutting diagonally across roadway bends rather than steering around."
    },
    "get cold feet": {
        "canonical_concept": "nervous_retreat",
        "language": "en",
        "phrase": "get cold feet",
        "idiom": "get cold feet",
        "aliases": ["get cold feet", "got cold feet", "getting cold feet", "gets cold feet"],
        "meaning": "To experience sudden intense nervousness, hesitation, or second thoughts before a committed action.",
        "example": "The groom got cold feet on the morning of the wedding ceremony.",
        "category": "Emotion & Hesitation",
        "idiomatic_keywords": ["nervous", "hesitate", "scared", "backing", "wedding", "speech", "fear", "anxious", "second", "confidence"],
        "literal_keywords": ["toes", "socks", "shoes", "frostbite", "temperature", "winter", "ice", "numb", "feet", "boots"],
        "usage_notes": "German literary idiom ('kalte Füße bekommen') adopted into English via 19th-century theater and military parlance."
    },
    "go the extra mile": {
        "canonical_concept": "exceed_obligations",
        "language": "en",
        "phrase": "go the extra mile",
        "idiom": "go the extra mile",
        "aliases": ["go the extra mile", "goes the extra mile", "going the extra mile", "went the extra mile"],
        "meaning": "To exert additional effort beyond what is strictly mandated or expected.",
        "example": "Our dedicated support staff went the extra mile to resolve the customer's urgent ticket.",
        "category": "Effort & Service",
        "idiomatic_keywords": ["effort", "dedication", "exceed", "service", "customer", "hard", "commitment", "quality", "satisfaction"],
        "literal_keywords": ["kilometer", "mile", "running", "hiking", "distance", "marathon", "walking", "odometer", "highway"],
        "usage_notes": "Biblical allusion to Roman soldiers requiring citizens to carry gear for one mile; believers volunteered to carry it two."
    },
    "jump on the bandwagon": {
        "canonical_concept": "adopt_popular_trend",
        "language": "en",
        "phrase": "jump on the bandwagon",
        "idiom": "jump on the bandwagon",
        "aliases": ["jump on the bandwagon", "jumped on the bandwagon", "jumping on the bandwagon", "jumps on the bandwagon"],
        "meaning": "To join a popular movement, trend, or cause solely because it has gained broad public traction.",
        "example": "Many venture capitalists jumped on the bandwagon of generative AI startups.",
        "category": "Social & Trends",
        "idiomatic_keywords": ["trend", "popular", "hype", "follow", "crowd", "fashion", "join", "adopt", "traction", "movement"],
        "literal_keywords": ["wagon", "parade", "circus", "brass", "band", "carriage", "instruments", "music", "musicians"],
        "usage_notes": "19th-century American political campaigns featured candidates riding on musical wagons to attract rallying crowds."
    },
    "miss the boat": {
        "canonical_concept": "forfeit_opportunity",
        "language": "en",
        "phrase": "miss the boat",
        "idiom": "miss the boat",
        "aliases": ["miss the boat", "missed the boat", "missing the boat", "misses the boat"],
        "meaning": "To fail to seize an advantageous opportunity due to delay or procrastination.",
        "example": "Investors who hesitated to buy shares early missed the boat on the stock's growth.",
        "category": "Opportunity & Timing",
        "idiomatic_keywords": ["opportunity", "late", "hesitated", "chance", "timing", "delayed", "missed", "growth", "regret"],
        "literal_keywords": ["ferry", "vessel", "dock", "pier", "harbor", "boarding", "ship", "captain", "water", "cruise"],
        "usage_notes": "Literal maritime reference to passengers who arrived at the shipping dock after the scheduled vessel had embarked."
    },
    "speak of the devil": {
        "canonical_concept": "person_arrives_when_mentioned",
        "language": "en",
        "phrase": "speak of the devil",
        "idiom": "speak of the devil",
        "aliases": ["speak of the devil", "speaking of the devil"],
        "meaning": "Said when an individual unexpectedly appears in person precisely while being spoken about.",
        "example": "We were just admiring John's presentation, and speak of the devil, here he comes.",
        "category": "Social & Coincidence",
        "idiomatic_keywords": ["arrived", "talking", "coincidence", "walked", "mentioning", "speak", "person", "enter", "presence"],
        "literal_keywords": ["demon", "satan", "evil", "folklore", "hell", "horns", "supernatural", "curse", "ritual"],
        "usage_notes": "Truncated form of the Latin proverb 'Lupus in fabula' ('the wolf in the story') warning against summoning trouble."
    },
    "through thick and thin": {
        "canonical_concept": "unwavering_loyalty",
        "language": "en",
        "phrase": "through thick and thin",
        "idiom": "through thick and thin",
        "aliases": ["through thick and thin"],
        "meaning": "Under all conditions, enduring both prosperous times and intense adversities with loyalty.",
        "example": "The childhood friends stood by each other through thick and thin for over forty years.",
        "category": "Loyalty & Friendship",
        "idiomatic_keywords": ["loyalty", "faithful", "support", "friendship", "hardship", "adversity", "devotion", "together", "bonds"],
        "literal_keywords": ["forest", "brambles", "vegetation", "woods", "thicket", "dense", "sparse", "branches", "mud"],
        "usage_notes": "Chaucerian phrase describing travelers pressing onward through dense thickets ('thick') and open pastures ('thin')."
    },
    "hit the sack": {
        "canonical_concept": "retire_to_sleep",
        "language": "en",
        "phrase": "hit the sack",
        "idiom": "hit the sack",
        "aliases": ["hit the sack", "hits the sack", "hitting the sack", "hit the hay"],
        "meaning": "To go to bed or fall asleep after a tiring day.",
        "example": "After a grueling twelve-hour shift, the nurse was ready to hit the sack.",
        "category": "Rest & Sleep",
        "idiomatic_keywords": ["sleep", "bed", "tired", "exhausted", "night", "rest", "fatigued", "shift", "slumber", "pillow"],
        "literal_keywords": ["sack", "bag", "potatoes", "burlap", "punch", "strike", "boxer", "gym", "grain", "flour"],
        "usage_notes": "Early 20th-century working-class and military slang referring to straw-filled burlap sacks used as rough mattresses."
    },
    "cry over spilled milk": {
        "canonical_concept": "futile_regret",
        "language": "en",
        "phrase": "cry over spilled milk",
        "idiom": "cry over spilled milk",
        "aliases": ["cry over spilled milk", "crying over spilled milk", "cried over spilled milk"],
        "meaning": "To waste time worrying or lamenting about a past mistake or loss that cannot be undone.",
        "example": "The contract is lost, but there is no use crying over spilled milk; let us focus on new clients.",
        "category": "Emotion & Resilience",
        "idiomatic_keywords": ["regret", "mistake", "past", "futile", "undo", "move", "forward", "worry", "loss"],
        "literal_keywords": ["milk", "dairy", "spill", "glass", "bottle", "jug", "counter", "puddle", "clean"],
        "usage_notes": "Proverb originating in 17th-century England advising stoic acceptance of unavoidable minor accidents."
    },
    "take with a grain of salt": {
        "canonical_concept": "healthy_skepticism",
        "language": "en",
        "phrase": "take with a grain of salt",
        "idiom": "take with a grain of salt",
        "aliases": ["take with a grain of salt", "taken with a grain of salt", "taking with a grain of salt"],
        "meaning": "To view a claim, story, or statement with healthy skepticism and not accept it completely as fact.",
        "example": "You should take online celebrity gossip with a grain of salt.",
        "category": "Belief & Truth",
        "idiomatic_keywords": ["skeptical", "doubt", "exaggerated", "rumor", "unverified", "caution", "claim", "story", "fact"],
        "literal_keywords": ["salt", "shaker", "grain", "sodium", "kitchen", "seasoning", "pinch", "taste", "mineral"],
        "usage_notes": "From Pliny the Elder's natural history regarding an antidote to poison taken with a grain of salt."
    },
    "burn bridges": {
        "canonical_concept": "irrevocable_break",
        "language": "en",
        "phrase": "burn bridges",
        "idiom": "burn bridges",
        "aliases": ["burn bridges", "burned bridges", "burning bridges", "burn his bridges", "burn her bridges"],
        "meaning": "To permanently destroy relations or eliminate pathways to return to a previous state.",
        "example": "Even if you dislike your current employer, do not burn bridges when resigning.",
        "category": "Relationships & Strategy",
        "idiomatic_keywords": ["resign", "employer", "relationships", "destroy", "permanent", "exit", "reputation", "hostile", "future"],
        "literal_keywords": ["bridge", "river", "fire", "timber", "planks", "arson", "crossing", "engineer", "stream"],
        "usage_notes": "Military tactic of burning river crossings behind advancing troops so retreat was physically impossible."
    },
    "at the drop of a hat": {
        "canonical_concept": "instant_readiness",
        "language": "en",
        "phrase": "at the drop of a hat",
        "idiom": "at the drop of a hat",
        "aliases": ["at the drop of a hat"],
        "meaning": "Willing or ready to do something immediately without any hesitation or prior planning.",
        "example": "My adventurous brother is ready to travel at the drop of a hat.",
        "category": "Readiness & Speed",
        "idiomatic_keywords": ["immediately", "instantly", "promptly", "hesitation", "willing", "spontaneous", "ready", "quick"],
        "literal_keywords": ["hat", "cap", "drop", "floor", "ground", "fell", "headwear", "wind"],
        "usage_notes": "Refers to the 19th-century practice of dropping a hat to signal the official start of a boxing match or foot race."
    },
    "apple of one's eye": {
        "canonical_concept": "cherished_favorite",
        "language": "en",
        "phrase": "apple of one's eye",
        "idiom": "apple of one's eye",
        "aliases": ["apple of one's eye", "apple of his eye", "apple of her eye", "apple of my eye"],
        "meaning": "A person who is cherished above all others, deeply loved and treasured.",
        "example": "His youngest granddaughter was the apple of his eye.",
        "category": "Affection & Family",
        "idiomatic_keywords": ["cherished", "treasure", "granddaughter", "favorite", "love", "precious", "darling", "adore", "family"],
        "literal_keywords": ["apple", "fruit", "orchard", "iris", "pupil", "eyeball", "vision", "cornea", "tree"],
        "usage_notes": "Ancient Old English expression for the pupil of the eye, essential to sight and carefully protected."
    },
    "leave no stone unturned": {
        "canonical_concept": "exhaustive_investigation",
        "language": "en",
        "phrase": "leave no stone unturned",
        "idiom": "leave no stone unturned",
        "aliases": ["leave no stone unturned", "left no stone unturned", "leaving no stone unturned"],
        "meaning": "To use every possible method, source, or effort to achieve an objective or solve a mystery.",
        "example": "The detectives left no stone unturned in their search for the missing heirloom.",
        "category": "Effort & Investigation",
        "idiomatic_keywords": ["investigation", "detectives", "search", "exhaustive", "thorough", "effort", "inquiry", "clues", "diligence"],
        "literal_keywords": ["stone", "rock", "pebble", "boulder", "ground", "lift", "soil", "quarry", "turn"],
        "usage_notes": "Attributed to the Oracle of Delphi advising Polycrates to seek hidden Persian treasure by turning every stone."
    },

    # ──────────────────────────────────────────────────────────────────────────
    # HINDI IDIOMS / मुहावरे (36 CANONICAL EXPRESSIONS)
    # ──────────────────────────────────────────────────────────────────────────
    "आँखों का तारा": {
        "canonical_concept": "cherished_favorite",
        "language": "hi",
        "phrase": "आँखों का तारा",
        "idiom": "आँखों का तारा",
        "aliases": ["आँखों का तारा", "आंखों का तारा", "आँख का तारा", "आंख का तारा"],
        "meaning": "अत्यधिक प्रिय अथवा बहुत प्यारा होना (Deeply loved and cherished person; apple of one's eye).",
        "example": "रोहन अपने माता-पिता की आँखों का तारा है।",
        "category": "Affection & Family",
        "idiomatic_keywords": ["प्यारा", "दुलारा", "माता-पिता", "बेटा", "लाडला", "स्नेह", "प्रिय", "परिवार"],
        "literal_keywords": ["तारा", "आसमान", "नक्षत्र", "दूरबीन", "नेत्र", "पलक", "पुतली", "रोशनी"],
        "usage_notes": "पारंपरिक हिंदी मुहावरा जो किसी संतान या अत्यंत प्रियजन के प्रति असीम प्रेम व्यक्त करता है।"
    },
    "भीगी बिल्ली बनना": {
        "canonical_concept": "timid_scared",
        "language": "hi",
        "phrase": "भीगी बिल्ली बनना",
        "idiom": "भीगी बिल्ली बनना",
        "aliases": ["भीगी बिल्ली बनना", "भीगी बिल्ली बन गया", "भीगी बिल्ली बन गई", "भीगी बिल्ली बनकर", "भीगी बिल्ली"],
        "meaning": "डरकर सहम जाना या अत्यंत दब्बू बन जाना (To cower in fear or act timid).",
        "example": "अध्यापक के कमरे में आते ही शरारती छात्र भीगी बिल्ली बन गया।",
        "category": "Emotion & Fear",
        "idiomatic_keywords": ["डर", "सहम", "शांत", "दब्बू", "घबराया", "चुपचाप", "अध्यापक", "माफी"],
        "literal_keywords": ["बिल्ली", "पानी", "बारिश", "नहाना", "गीली", "पंजे", "फर", "म्याऊं"],
        "usage_notes": "पानी में भीगने के बाद बिल्ली की दयनीय और शांत स्थिति से तुलना की जाती है।"
    },
    "हाथ खींचना": {
        "canonical_concept": "withdraw_support",
        "language": "hi",
        "phrase": "हाथ खींचना",
        "idiom": "हाथ खींचना",
        "aliases": ["हाथ खींचना", "हाथ खींच लिया", "हाथ खींच लिए", "हाथ खींच रहे हैं"],
        "meaning": "सहायता बंद करना या समर्थन से पीछे हट जाना (To withdraw assistance or financial aid).",
        "example": "व्यापार में घाटा होते ही साझेदार ने निवेश से हाथ खींच लिया।",
        "category": "Support & Commitment",
        "idiomatic_keywords": ["मदद", "साझेदार", "सहायता", "घाटा", "समर्थन", "इनकार", "व्यापार", "अलग"],
        "literal_keywords": ["हाथ", "खींचना", "अंगुली", "पकड़", "तौलिया", "आग", "गर्म", "स्पर्श"],
        "usage_notes": "सामाजिक अथवा वित्तीय संबंध में सहयोग वापस लेने के संदर्भ में प्रयुक्त।"
    },
    "अंगूठा दिखाना": {
        "canonical_concept": "flat_refusal",
        "language": "hi",
        "phrase": "अंगूठा दिखाना",
        "idiom": "अंगूठा दिखाना",
        "aliases": ["अंगूठा दिखाना", "अंगूठा दिखा दिया", "अंगूठा दिखाती है", "अंगूठा दिखाकर"],
        "meaning": "वक्त पर साफ़ मना कर देना अथवा धोखा देना (To refuse outright at the critical moment).",
        "example": "जब मैंने मित्र से उधार माँगा, तो उसने साफ़ अंगूठा दिखा दिया।",
        "category": "Communication & Refusal",
        "idiomatic_keywords": ["मना", "इनकार", "धोखा", "वक्त", "सहायता", "मित्र", "उधार", "मुकर"],
        "literal_keywords": ["अंगूठा", "हाथ", "अंगुलियां", "संकेत", "हथेली", "चित्र", "मुट्ठी"],
        "usage_notes": "ऐन वक्त पर सहायता देने के वादे से मुकर जाने के लिए अत्यंत लोकप्रिय मुहावरा।"
    },
    "दाल में काला": {
        "canonical_concept": "something_fishy",
        "language": "hi",
        "phrase": "दाल में काला",
        "idiom": "दाल में काला",
        "aliases": ["दाल में काला", "दाल में कुछ काला", "दाल में बहुत कुछ काला"],
        "meaning": "किसी बात में संदेह होना या कुछ गड़बड़ होना (Something suspicious or fishy going on).",
        "example": "उसकी अजीब बातों से लग रहा था कि दाल में कुछ काला है।",
        "category": "Suspicion & Mystery",
        "idiomatic_keywords": ["संदेह", "गड़बड़", "शक", "रहस्य", "छुपा", "घपला", "जांच", "चालाकी"],
        "literal_keywords": ["दाल", "काला", "कंकड़", "पकाना", "रसोई", "कटोरी", "अनाज", "मसाला"],
        "usage_notes": "दाल पकाते समय उसमें गिरे किसी काले कंकड़ से उपजी उपमा, जो विसंगति को दर्शाती है।"
    },
    "हवा से बातें करना": {
        "canonical_concept": "extreme_speed",
        "language": "hi",
        "phrase": "हवा से बातें करना",
        "idiom": "हवा से बातें करना",
        "aliases": ["हवा से बातें करना", "हवा से बातें कर रहा", "हवा से बातें करने लगा", "हवा से बातें करती"],
        "meaning": "बहुत तेज़ गति से दौड़ना या चलना (To move or travel at lightning speed).",
        "example": "महाराणा प्रताप का चेतक युद्ध के मैदान में हवा से बातें करता था।",
        "category": "Speed & Motion",
        "idiomatic_keywords": ["तेज़", "दौड़ना", "रफ़्तार", "घोड़ा", "गाड़ी", "तीव्र", "दौड़", "उड़ान"],
        "literal_keywords": ["हवा", "वायु", "बातचीत", "बोलना", "तूफान", "ध्वनि", "मौसम", "सांस"],
        "usage_notes": "गति की तीव्रता को व्यक्त करने के लिए वीरगाथाओं और सामान्य भाषा में प्रयुक्त।"
    },
    "गाल बजाना": {
        "canonical_concept": "boasting_bragging",
        "language": "hi",
        "phrase": "गाल बजाना",
        "idiom": "गाल बजाना",
        "aliases": ["गाल बजाना", "गाल बजाता है", "गाल बजाने लगा", "गाल बजा रहे"],
        "meaning": "व्यर्थ की डींगें मारना या शेखी बघारना (To boast, brag, or talk loudly without substance).",
        "example": "सफलता कर्म करने से मिलती है, केवल गाल बजाने से नहीं।",
        "category": "Speech & Arrogance",
        "idiomatic_keywords": ["डींग", "शेखी", "झूठी", "प्रशंसा", "बड़बोला", "अहंकार", "बातें", "दिखावा"],
        "literal_keywords": ["गाल", "थप्पड़", "चेहरा", "हाथ", "ताली", "आवाज़", "मुंह", "त्वचा"],
        "usage_notes": "कर्महीन व्यक्ति द्वारा केवल बढ़-चढ़कर बोलने की प्रवृत्ति पर कटाक्ष।"
    },
    "आस्तीन का सांप": {
        "canonical_concept": "hidden_traitor",
        "language": "hi",
        "phrase": "आस्तीन का सांप",
        "idiom": "आस्तीन का सांप",
        "aliases": ["आस्तीन का सांप", "आस्तीन का साँप"],
        "meaning": "मित्र के वेश में छुपा हुआ कपटी अथवा विश्वासघाती व्यक्ति (A treacherous friend in disguise).",
        "example": "रमेश जिसे सच्चा दोस्त समझता था, वह आस्तीन का सांप निकला।",
        "category": "Deception & Betrayal",
        "idiomatic_keywords": ["धोखेबाज़", "विश्वासघात", "कपटी", "गद्दार", "दुश्मन", "साजिश", "मित्र", "छल"],
        "literal_keywords": ["सांप", "आस्तीन", "कुर्ता", "जहरीला", "डंक", "कपड़ा", "सरीसृप", "फन"],
        "usage_notes": "अपने निकटतम व्यक्ति द्वारा किए जाने वाले विश्वासघात को निरूपित करता है।"
    },
    "लोहे के चने चबाना": {
        "canonical_concept": "extremely_tough_task",
        "language": "hi",
        "phrase": "लोहे के चने चबाना",
        "idiom": "लोहे के चने चबाना",
        "aliases": ["लोहे के चने चबाना", "लोहे के चने चबाने पड़े", "लोहे के चने चबा दिए"],
        "meaning": "अत्यंत कठिन चुनौती या भयंकर कठिनाई का सामना करना (To tackle an immensely arduous task).",
        "example": "सिविल सेवा परीक्षा उत्तीर्ण करना लोहे के चने चबाने के समान है।",
        "category": "Challenge & Grit",
        "idiomatic_keywords": ["कठिन", "चुनौती", "परिश्रम", "परीक्षा", "मुश्किल", "संघर्ष", "साधना", "असंभव"],
        "literal_keywords": ["चना", "लोहा", "दांत", "भोजन", "चबाना", "धातु", "कठोर", "थाली"],
        "usage_notes": "असंभव प्रतीत होने वाले कठिन कार्य को करने के संघर्ष का सटीक चित्रण।"
    },
    "कान भरना": {
        "canonical_concept": "poisoning_ears",
        "language": "hi",
        "phrase": "कान भरना",
        "idiom": "कान भरना",
        "aliases": ["कान भरना", "कान भर दिए", "कान भरता है", "कान भर रही है"],
        "meaning": "किसी के विरुद्ध चुगली करना अथवा भड़काना (To poison someone's mind with gossip or slander).",
        "example": "पड़ोसी ने प्रबंधक के कान भरकर दोनों भाइयों में झगड़ा करा दिया।",
        "category": "Deception & Conflict",
        "idiomatic_keywords": ["चुगली", "भड़काना", "झगड़ा", "शिकायत", "द्वेष", "झूठ", "गलतफहमी", "मनमुटाव"],
        "literal_keywords": ["कान", "पानी", "रूई", "भरना", "मैल", "सुनना", "दवा", "बूंद"],
        "usage_notes": "किसी के मन में तीसरे व्यक्ति के प्रति दुर्भावना उत्पन्न करने के अर्थ में प्रयुक्त।"
    },
    "पीठ थपथपाना": {
        "canonical_concept": "pat_on_back",
        "language": "hi",
        "phrase": "पीठ थपथपाना",
        "idiom": "पीठ थपथपाना",
        "aliases": ["पीठ थपथपाना", "पीठ थपथपाई", "पीठ थपथपाते हुए", "पीठ थपथपा कर"],
        "meaning": "शाबाशी देना, हौसला बढ़ाना अथवा प्रशंसा करना (To congratulate, encourage, or praise).",
        "example": "गणित प्रतियोगिता जीतने पर प्रधानाचार्य ने छात्र की पीठ थपथपाई।",
        "category": "Praise & Encouragement",
        "idiomatic_keywords": ["शाबाशी", "प्रशंसा", "हौसला", "सफलता", "इनाम", "जीत", "उत्साह", "प्रोत्साहन"],
        "literal_keywords": ["पीठ", "हाथ", "थपकी", "कंधा", "स्पर्श", "शरीर", "मालिश", "दर्द"],
        "usage_notes": "सराहना और स्नेह व्यक्त करने की स्वाभाविक शारीरिक क्रिया से बना मुहावरा।"
    },
    "ईंट का जवाब पत्थर से देना": {
        "canonical_concept": "tit_for_tat",
        "language": "hi",
        "phrase": "ईंट का जवाब पत्थर से देना",
        "idiom": "ईंट का जवाब पत्थर से देना",
        "aliases": ["ईंट का जवाब पत्थर से देना", "ईंट का जवाब पत्थर से दिया"],
        "meaning": "शत्रु के प्रहार का उससे भी अधिक कठोरता से प्रत्युत्तर देना (To retaliate with even greater force).",
        "example": "भारतीय सेना ने सीमा पर घुसपैठियों को ईंट का जवाब पत्थर से दिया।",
        "category": "Conflict & Retaliation",
        "idiomatic_keywords": ["जवाब", "मुंहतोड़", "बदला", "शत्रु", "वीरता", "सामना", "करारा", "सैनिक"],
        "literal_keywords": ["ईंट", "पत्थर", "दीवार", "फेंकना", "चोट", "निर्माण", "मकान", "मलबे"],
        "usage_notes": "प्रतिशोध और शौर्यपूर्ण प्रतिवाद को दर्शाने वाला सशक्त मुहावरा।"
    },
    "दिन-रात एक करना": {
        "canonical_concept": "burn_the_midnight_oil",
        "language": "hi",
        "phrase": "दिन-रात एक करना",
        "idiom": "दिन-रात एक करना",
        "aliases": ["दिन-रात एक करना", "दिन-रात एक कर दिया", "दिन-रात एक कर दी"],
        "meaning": "अत्यधिक कठोर परिश्रम करना (To work day and night with immense dedication).",
        "example": "बोर्ड परीक्षा में प्रथम आने के लिए उसने दिन-रात एक कर दिया।",
        "category": "Effort & Work",
        "idiomatic_keywords": ["परिश्रम", "मेहनत", "लगन", "पढ़ाई", "परीक्षा", "प्रयास", "सफलता", "अभ्यास"],
        "literal_keywords": ["दिन", "रात", "सूरज", "चांद", "घड़ी", "समय", "चौबीस", "सुबह", "शाम"],
        "usage_notes": "अंग्रेजी 'burn the midnight oil' का अत्यंत स्वाभाविक और प्रामाणिक हिंदी पर्याय।"
    },
    "अंगारे उगलना": {
        "canonical_concept": "furious_speech",
        "language": "hi",
        "phrase": "अंगारे उगलना",
        "idiom": "अंगारे उगलना",
        "aliases": ["अंगारे उगलना", "अंगारे उगलने लगा", "अंगारे उगल रही थी"],
        "meaning": "क्रोध में अत्यंत कटु, तीखे अथवा अपमानजनक शब्द कहना (To speak with blazing fury and malice).",
        "example": "विवाद बढ़ने पर वह विपक्षी दल पर अंगारे उगलने लगा।",
        "category": "Emotion & Anger",
        "idiomatic_keywords": ["क्रोध", "गुस्सा", "कटु", "तीखे", "अपमान", "चिल्लाना", "नाराजगी", "भाषण"],
        "literal_keywords": ["अंगारे", "कोयला", "आग", "ज्वाला", "राख", "उगलना", "मुंह", "भट्टी"],
        "usage_notes": "क्रोध से भरे विषैले शब्दों की ज्वाला से तुलना।"
    },
    "आँखों में धूल झोंकना": {
        "canonical_concept": "deceive_someone",
        "language": "hi",
        "phrase": "आँखों में धूल झोंकना",
        "idiom": "आँखों में धूल झोंकना",
        "aliases": ["आँखों में धूल झोंकना", "आंखों में धूल झोंक दी", "आँखों में धूल झोंककर"],
        "meaning": "धोखा देना अथवा भ्रमित करके भाग निकलना (To deceive or pull wool over someone's eyes).",
        "example": "शातिर चोर पुलिस की आँखों में धूल झोंककर फरार हो गया।",
        "category": "Deception & Crime",
        "idiomatic_keywords": ["धोखा", "फरार", "चोर", "चालाकी", "चकमा", "छल", "बच", "अपराध"],
        "literal_keywords": ["धूल", "मिट्टी", "आंख", "झोंकना", "हवा", "आंधी", "रेत", "कण"],
        "usage_notes": "दृष्टि भ्रमित कर कपट करने की स्थिति का रूपक।"
    },
    "उड़ती चिड़िया पहचानना": {
        "canonical_concept": "sharp_intuition",
        "language": "hi",
        "phrase": "उड़ती चिड़िया पहचानना",
        "idiom": "उड़ती चिड़िया पहचानना",
        "aliases": ["उड़ती चिड़िया पहचानना", "उड़ती चिड़िया पहचानते हैं", "उड़ती चिड़िया पहचान ली"],
        "meaning": "दूर से ही किसी के गुप्त इरादे या मनोभाव भांप लेना (To possess keen discernment or intuition).",
        "example": "हमारे दादाजी इतने अनुभवी हैं कि वे उड़ती चिड़िया पहचान लेते हैं।",
        "category": "Wisdom & Intuition",
        "idiomatic_keywords": ["अनुभवी", "भांप", "पहचान", "इरादा", "मन", "चालाकी", "समझदार", "बुद्धि"],
        "literal_keywords": ["चिड़िया", "पक्षी", "उड़ना", "आसमान", "पंख", "घोंसला", "पेड़", "नजर"],
        "usage_notes": "व्यावहारिक ज्ञान और गहरी अंतर्दृष्टि के लिए प्रयुक्त।"
    },
    "कलेजे पर सांप लोटना": {
        "canonical_concept": "burning_with_envy",
        "language": "hi",
        "phrase": "कलेजे पर सांप लोटना",
        "idiom": "कलेजे पर सांप लोटना",
        "aliases": ["कलेजे पर सांप लोटना", "कलेजे पर सांप लोटने लगा", "कलेजे पर सांप लोट गया"],
        "meaning": "किसी की तरक्की अथवा संपत्ति देखकर तीव्र ईर्ष्या से जलना (To burn with agonizing jealousy).",
        "example": "पड़ोसी की नई गाड़ी देखकर शर्माजी के कलेजे पर सांप लोटने लगा।",
        "category": "Emotion & Envy",
        "idiomatic_keywords": ["ईर्ष्या", "जलन", "तरक्की", "द्वेष", "सफलता", "सहन", "कुढ़न", "दुख"],
        "literal_keywords": ["सांप", "कलेजा", "छाती", "लोटना", "जहर", "फन", "रेंगना", "हृदय"],
        "usage_notes": "तीव्र डाह और मानसिक बेचैनी का प्रतीकात्मक चित्रण।"
    },
    "खून का घूंट पीना": {
        "canonical_concept": "swallowing_humiliation",
        "language": "hi",
        "phrase": "खून का घूंट पीना",
        "idiom": "खून का घूंट पीना",
        "aliases": ["खून का घूंट पीना", "खून का घूंट पीकर", "खून का घूंट पी लिया"],
        "meaning": "भारी अपमान या अन्याय को विवश होकर चुपचाप सह लेना (To swallow humiliation in silence).",
        "example": "अधिकारी के कटु वचनों को सुनकर कर्मचारी खून का घूंट पीकर रह गया।",
        "category": "Emotion & Resilience",
        "idiomatic_keywords": ["अपमान", "चुपचाप", "सहन", "विवश", "क्रोध", "धैर्य", "लाचार", "बेबसी"],
        "literal_keywords": ["खून", "रक्त", "घूंट", "पीना", "गिलास", "ओष्ठ", "चोट", "घाव"],
        "usage_notes": "मजबूरी में आत्मसम्मान पर लगे आघात को सहने की वेदना।"
    },
    "घड़ों पानी पड़ना": {
        "canonical_concept": "deeply_ashamed",
        "language": "hi",
        "phrase": "घड़ों पानी पड़ना",
        "idiom": "घड़ों पानी पड़ना",
        "aliases": ["घड़ों पानी पड़ना", "घड़ों पानी पड़ गया", "घड़ों पानी पड़ा"],
        "meaning": "अत्यंत लज्जित अथवा शर्मिंदा होना (To be overwhelmed by profound shame and embarrassment).",
        "example": "जब उसकी चोरी पकड़ी गई, तो उसके चेहरे पर घड़ों पानी पड़ गया।",
        "category": "Emotion & Shame",
        "idiomatic_keywords": ["लज्जित", "शर्मिंदा", "अपराध", "चोरी", "पकड़े", "ग्लानि", "झुका", "शर्म"],
        "literal_keywords": ["घड़ा", "पानी", "मटका", "नहाना", "बूंद", "नदी", "भीगना", "बरसात"],
        "usage_notes": "अपमान और अपराधबोध से उत्पन्न पसीने व स्तब्धता की उपमा।"
    },
    "चांदी काटना": {
        "canonical_concept": "making_easy_fortune",
        "language": "hi",
        "phrase": "चांदी काटना",
        "idiom": "चांदी काटना",
        "aliases": ["चांदी काटना", "चांदी काट रहा है", "चांदी काट रहे हैं"],
        "meaning": "खूब धन कमाना अथवा खूब मौज-मस्ती में रहना (To rake in riches or make easy fortune).",
        "example": "त्योहारों के मौसम में मिठाई विक्रेता खूब चांदी काट रहे हैं।",
        "category": "Wealth & Success",
        "idiomatic_keywords": ["धन", "कमाई", "मुनाफा", "व्यापार", "मौज", "दौलत", "बिक्री", "अमीर"],
        "literal_keywords": ["चांदी", "काटना", "धातु", "सिक्का", "कैंची", "आभूषण", "सुनार", "चम्मच"],
        "usage_notes": "अचानक भरपूर मुनाफा होने की स्थिति को व्यक्त करता है।"
    },
    "चिराग तले अंधेरा": {
        "canonical_concept": "darkness_under_lamp",
        "language": "hi",
        "phrase": "चिराग तले अंधेरा",
        "idiom": "चिराग तले अंधेरा",
        "aliases": ["चिराग तले अंधेरा", "दीपक तले अंधेरा"],
        "meaning": "ज्ञानदाता या उच्च पदस्थ व्यक्ति के अपने ही घर में अज्ञान या बुराई होना (Darkness under one's own lamp).",
        "example": "अध्यापक का अपना बेटा ही परीक्षा में अनुत्तीर्ण हो गया, इसे कहते हैं चिराग तले अंधेरा।",
        "category": "Irony & Wisdom",
        "idiomatic_keywords": ["विडंबना", "दोष", "घर", "अज्ञान", "उलट", "अध्यापक", "बुराई", "नियम"],
        "literal_keywords": ["चिराग", "दीपक", "अंधेरा", "लौ", "तेल", "बाती", "रोशनी", "छाया"],
        "usage_notes": "दीपक की लौ नीचे पड़ने वाली स्वाभाविक छाया से प्रेरित प्रसिद्ध लोकोक्ति/मुहावरा।"
    },
    "छक्के छुड़ाना": {
        "canonical_concept": "crush_opposition",
        "language": "hi",
        "phrase": "छक्के छुड़ाना",
        "idiom": "छक्के छुड़ाना",
        "aliases": ["छक्के छुड़ाना", "छक्के छुड़ा दिए", "छक्के छुड़ा देगा"],
        "meaning": "बुरी तरह पराजित करना अथवा होश उड़ा देना (To defeat thoroughly or demoralize the opponent).",
        "example": "भारतीय क्रिकेट टीम ने फाइनल मुकाबले में विपक्षी के छक्के छुड़ा दिए।",
        "category": "Victory & Defeat",
        "idiomatic_keywords": ["पराजित", "जीत", "मैच", "मुकाबला", "धूल", "होश", "क्रिकेट", "सैनिक"],
        "literal_keywords": ["छक्का", "गेंद", "बल्ला", "बाउंड्री", "छह", "ताश", "खेल"],
        "usage_notes": "युद्ध अथवा खेल में प्रतिद्वंद्वी को पूर्णतः पस्त करने के लिए प्रयुक्त।"
    },
    "जले पर नमक छिड़कना": {
        "canonical_concept": "add_salt_to_wound",
        "language": "hi",
        "phrase": "जले पर नमक छिड़कना",
        "idiom": "जले पर नमक छिड़कना",
        "aliases": ["जले पर नमक छिड़कना", "जले पर नमक छिड़क दिया", "जले पर नमक छिड़कते हुए"],
        "meaning": "दुखी व्यक्ति को ताने मारकर और अधिक व्यथित करना (To add insult to injury / salt to a wound).",
        "example": "व्यापार में असफलता के बाद रिश्तेदारों के तानों ने जले पर नमक छिड़क दिया।",
        "category": "Cruelty & Pain",
        "idiomatic_keywords": ["ताना", "दुख", "व्यथा", "पीड़ा", "मजाक", "असफलता", "दर्द", "कष्ट"],
        "literal_keywords": ["जला", "नमक", "घाव", "छिड़कना", "चमड़ी", "आग", "रस", "मलहम"],
        "usage_notes": "अंग्रेजी 'rub salt into the wound' का सटीक और प्रामाणिक हिंदी मुहावरा।"
    },
    "टांग अड़ाना": {
        "canonical_concept": "interfering_meddling",
        "language": "hi",
        "phrase": "टांग अड़ाना",
        "idiom": "टांग अड़ाना",
        "aliases": ["टांग अड़ाना", "टांग अड़ाता है", "टांग अड़ाने लगा", "टांग अड़ाती है"],
        "meaning": "दूसरों के कार्य में व्यर्थ का हस्तक्षेप करना या बाधा डालना (To meddle or interfere unnecessarily).",
        "example": "हर बात में बिना वजह टांग अड़ाना तुम्हारी बहुत बुरी आदत है।",
        "category": "Conflict & Meddling",
        "idiomatic_keywords": ["दखल", "हस्तक्षेप", "बाधा", "अड़चन", "बेवजह", "काम", "आदत", "विवाद"],
        "literal_keywords": ["टांग", "पैर", "फंसाना", "रास्ता", "गिरना", "घुटने", "चलना"],
        "usage_notes": "चलते व्यक्ति के पैर में पैर अड़ाकर गिराने की चेष्टा से बना मुहावरा।"
    },
    "दम तोड़ना": {
        "canonical_concept": "breathe_last",
        "language": "hi",
        "phrase": "दम तोड़ना",
        "idiom": "दम तोड़ना",
        "aliases": ["दम तोड़ना", "दम तोड़ दिया", "दम तोड़ रहा है"],
        "meaning": "प्राण त्याग देना, मृत्यु होना अथवा समाप्त हो जाना (To breathe one's last / pass away).",
        "example": "गंभीर रूप से घायल मरीज ने अस्पताल पहुँचते ही दम तोड़ दिया।",
        "category": "Life & Mortality",
        "idiomatic_keywords": ["मृत्यु", "प्राण", "अस्पताल", "मरीज", "हादसा", "निधन", "अंत", "घायल"],
        "literal_keywords": ["दम", "सांस", "तोड़ना", "हवा", "फेफड़े", "गला", "रस्सी", "धागा"],
        "usage_notes": "मानव जीवन अथवा किसी आंदोलन के अंत को व्यक्त करने हेतु प्रयुक्त।"
    },
    "दांत खट्टे करना": {
        "canonical_concept": "humiliate_defeat",
        "language": "hi",
        "phrase": "दांत खट्टे करना",
        "idiom": "दांत खट्टे करना",
        "aliases": ["दांत खट्टे करना", "दांत खट्टे कर दिए", "दांत खट्टे कर दिए थे"],
        "meaning": "शत्रु को बुरी तरह परास्त करना या छका देना (To make someone taste bitter defeat).",
        "example": "रानी लक्ष्मीबाई ने अंग्रेजों की सेना के दांत खट्टे कर दिए थे।",
        "category": "Bravery & Defeat",
        "idiomatic_keywords": ["परास्त", "शत्रु", "युद्ध", "अंग्रेज", "वीरता", "लड़ाई", "हार", "सेना"],
        "literal_keywords": ["दांत", "खट्टा", "नींबू", "इमली", "स्वाद", "मुंह", "मसूड़े", "फल"],
        "usage_notes": "अत्यधिक खट्टी वस्तु खाने से दांतों में उत्पन्न झनझनाहट के रूपक से बना मुहावरा।"
    },
    "धज्जियां उड़ाना": {
        "canonical_concept": "tear_to_shreds",
        "language": "hi",
        "phrase": "धज्जियां उड़ाना",
        "idiom": "धज्जियां उड़ाना",
        "aliases": ["धज्जियां उड़ाना", "धज्जियां उड़ा दीं", "धज्जियां उड़ा दी"],
        "meaning": "कठोर आलोचना करना अथवा प्रतिष्ठा को पूर्णतः खंडित कर देना (To tear to shreds / dismantle completely).",
        "example": "वकील ने अपनी तीखी दलीलों से झूठे गवाह की धज्जियां उड़ा दीं।",
        "category": "Criticism & Destruction",
        "idiomatic_keywords": ["आलोचना", "दलील", "वकील", "झूठ", "प्रतिष्ठा", "बहस", "सच्चाई", "नष्ट"],
        "literal_keywords": ["धज्जियां", "कपड़ा", "टुकड़े", "उड़ाना", "हवा", "फाड़ना", "कागज", "धागे"],
        "usage_notes": "कपड़े के चिथड़े उड़ाने के दृश्य से तर्क अथवा नियम की दुर्गति दर्शाना।"
    },
    "नमक-मिर्च लगाना": {
        "canonical_concept": "exaggerate_drama",
        "language": "hi",
        "phrase": "नमक-मिर्च लगाना",
        "idiom": "नमक-मिर्च लगाना",
        "aliases": ["नमक-मिर्च लगाना", "नमक-मिर्च लगाकर", "नमक मिर्च लगाना"],
        "meaning": "किसी सामान्य बात को बढ़ा-चढ़ाकर और चटपटी बनाकर प्रस्तुत करना (To exaggerate or sensationalize).",
        "example": "अखबार के संवाददाता ने घटना को नमक-मिर्च लगाकर पेश किया।",
        "category": "Speech & Exaggeration",
        "idiomatic_keywords": ["बढ़ा-चढ़ाकर", "चटपटी", "अफवाह", "संवाददाता", "बात", "बयान", "झूठ", "नाटक"],
        "literal_keywords": ["नमक", "मिर्च", "मसाला", "खाना", "सब्जी", "छिड़कना", "रसोई", "स्वाद"],
        "usage_notes": "समाचार अथवा गपशप में कृत्रिम सनसनी जोड़ने की प्रवृत्ति पर प्रयुक्त।"
    },
    "नौ दो ग्यारह होना": {
        "canonical_concept": "flee_rapidly",
        "language": "hi",
        "phrase": "नौ दो ग्यारह होना",
        "idiom": "नौ दो ग्यारह होना",
        "aliases": ["नौ दो ग्यारह होना", "नौ दो ग्यारह हो गया", "नौ दो ग्यारह हो गए"],
        "meaning": "डर या पकड़े जाने के भय से तुरंत भाग जाना (To flee rapidly / run away).",
        "example": "पुलिस की गाड़ी देखते ही जेबकतरे नौ दो ग्यारह हो गए।",
        "category": "Action & Escape",
        "idiomatic_keywords": ["भाग", "फरार", "पुलिस", "डर", "गायब", "चोर", "रफूचक्कर", "दौड़"],
        "literal_keywords": ["नौ", "दो", "ग्यारह", "गिनती", "संख्या", "गणित", "जोड़", "अंक"],
        "usage_notes": "अंकगणितीय संख्या (9 + 2 = 11) से द्रुत गति से प्रस्थान को सूचित करता प्रसिद्ध मुहावरा।"
    },
    "पहाड़ टूटना": {
        "canonical_concept": "catastrophic_calamity",
        "language": "hi",
        "phrase": "पहाड़ टूटना",
        "idiom": "पहाड़ टूटना",
        "aliases": ["पहाड़ टूटना", "पहाड़ टूट पड़ा", "पहाड़ टूट पड़े"],
        "meaning": "अचानक भारी विपत्ति या असह्य संकट आ पड़ना (A catastrophe or overwhelming calamity strikes).",
        "example": "परिवार के एकमात्र कमाने वाले के निधन से उन पर दुखों का पहाड़ टूट पड़ा।",
        "category": "Misfortune & Tragedy",
        "idiomatic_keywords": ["संकट", "विपत्ति", "दुख", "त्रासदी", "कठिनाई", "परिवार", "आघात", "अकेला"],
        "literal_keywords": ["पहाड़", "चट्टान", "पत्थर", "टूटना", "भूस्खलन", "पर्वत", "मलबे", "धंसना"],
        "usage_notes": "अचानक आई असह्य आपदा के भार को अभिव्यक्त करता है।"
    },
    "फूला न समाना": {
        "canonical_concept": "bursting_with_joy",
        "language": "hi",
        "phrase": "फूला न समाना",
        "idiom": "फूला न समाना",
        "aliases": ["फूला न समाना", "फूला न समाया", "फूली न समाई", "फूले न समाए"],
        "meaning": "अत्यधिक प्रसन्न होना अथवा आनंद से विभोर हो जाना (To be overflowing with immense joy).",
        "example": "आईएएस परीक्षा में चयन होने का समाचार पाकर वह फूला न समाया।",
        "category": "Emotion & Happiness",
        "idiomatic_keywords": ["प्रसन्न", "खुशी", "आनंद", "उत्साह", "सफलता", "समाचार", "गदगद", "बधाई"],
        "literal_keywords": ["फूल", "समाना", "पेट", "सांस", "गुब्बारा", "कपड़ा", "आकार"],
        "usage_notes": "हृदय में खुशी के समा न पाने की पराकाष्ठा का भाव।"
    },
    "बाल की खाल निकालना": {
        "canonical_concept": "splitting_hairs",
        "language": "hi",
        "phrase": "बाल की खाल निकालना",
        "idiom": "बाल की खाल निकालना",
        "aliases": ["बाल की खाल निकालना", "बाल की खाल निकालता है", "बाल की खाल निकालने लगे"],
        "meaning": "व्यर्थ की अत्यधिक सूक्ष्म छानबीन करना या मीन-मेख निकालना (To split hairs or over-scrutinize minutely).",
        "example": "हर साधारण नियम पर बाल की खाल निकालना अच्छे प्रबंधकों का काम नहीं।",
        "category": "Criticism & Scrutiny",
        "idiomatic_keywords": ["मीन-मेख", "बारीक", "छानबीन", "दोष", "बहस", "तर्क", "आपत्ति", "खामियां"],
        "literal_keywords": ["बाल", "खाल", "चमड़ी", "सिर", "काटना", "नाखून", "सूई", "शरीर"],
        "usage_notes": "अनावश्यक नुक्ताचीनी करने की आदत पर कटाक्ष।"
    },
    "राई का पहाड़ बनाना": {
        "canonical_concept": "mountain_of_molehill",
        "language": "hi",
        "phrase": "राई का पहाड़ बनाना",
        "idiom": "राई का पहाड़ बनाना",
        "aliases": ["राई का पहाड़ बनाना", "राई का पहाड़ बना दिया", "राई का पहाड़ बना रहे"],
        "meaning": "छोटी सी बात को बहुत बड़ा बतंगड़ बना देना (To make a mountain out of a molehill).",
        "example": "एक छोटी सी नोकझोंक पर राई का पहाड़ बनाकर उसने संबंध तोड़ लिए।",
        "category": "Conflict & Exaggeration",
        "idiomatic_keywords": ["बतंगड़", "छोटी", "झगड़ा", "विवाद", "बढ़ावा", "नासमझी", "बात", "क्रोध"],
        "literal_keywords": ["राई", "दाना", "पहाड़", "सरसों", "मसाला", "चट्टान", "ढेर", "भूमि"],
        "usage_notes": "अंग्रेजी 'make a mountain out of a molehill' का परिपक्व और लोकप्रिय हिंदी रूपांतर।"
    },
    "रंग में भंग पड़ना": {
        "canonical_concept": "spoil_festivities",
        "language": "hi",
        "phrase": "रंग में भंग पड़ना",
        "idiom": "रंग में भंग पड़ना",
        "aliases": ["रंग में भंग पड़ना", "रंग में भंग पड़ गया", "रंग में भंग डाल दिया"],
        "meaning": "उल्लास, आनंद अथवा उत्सव में अप्रत्याशित बाधा आ जाना (To spoil the fun or dampen festivities).",
        "example": "शादी के जश्न में बिजली चले जाने से रंग में भंग पड़ गया।",
        "category": "Disruption & Mood",
        "idiomatic_keywords": ["बाधा", "उत्सव", "जश्न", "आनंद", "खलल", "शादी", "मजा", "किरकिरा"],
        "literal_keywords": ["रंग", "भंग", "घोलना", "कपड़ा", "होली", "पेय", "नशा", "पाउडर"],
        "usage_notes": "समारोह के सुखद माहौल के अचानक बिगड़ने के लिए प्रयुक्त।"
    },
    "हाथ धोकर पीछे पड़ना": {
        "canonical_concept": "hound_relentlessly",
        "language": "hi",
        "phrase": "हाथ धोकर पीछे पड़ना",
        "idiom": "हाथ धोकर पीछे पड़ना",
        "aliases": ["हाथ धोकर पीछे पड़ना", "हाथ धोकर पीछे पड़ गया", "हाथ धोकर पीछे पड़ गए"],
        "meaning": "किसी कार्य अथवा व्यक्ति के पीछे पूरी तरह लग जाना और पीछा न छोड़ना (To pursue relentlessly).",
        "example": "ऋण वसूली अधिकारी बकाया राशि के लिए उसके हाथ धोकर पीछे पड़ गया।",
        "category": "Persistence & Harassment",
        "idiomatic_keywords": ["पीछा", "तंग", "वसूल", "जिद", "परेशान", "लगातार", "दबाव", "अधिकारी"],
        "literal_keywords": ["हाथ", "धोना", "साबुन", "पानी", "बेसिन", "तौलिया", "कदम", "चलना"],
        "usage_notes": "किसी उद्देश्य या व्यक्ति के प्रति अवांछित एकाग्रता व हठ को व्यक्त करता है।"
    },
    "हथियार डालना": {
        "canonical_concept": "surrender_arms",
        "language": "hi",
        "phrase": "हथियार डालना",
        "idiom": "हथियार डालना",
        "aliases": ["हथियार डालना", "हथियार डाल दिए", "हथियार डालने पड़े"],
        "meaning": "हार मान लेना अथवा आत्मसमर्पण कर देना (To surrender or concede defeat).",
        "example": "घिर जाने के बाद विद्रोही सैनिकों को सेना के सामने हथियार डालने पड़े।",
        "category": "Defeat & Surrender",
        "idiomatic_keywords": ["हार", "समर्पण", "पराजय", "सैनिक", "झुकना", "मजबूर", "स्वीकार", "युद्ध"],
        "literal_keywords": ["हथियार", "बंदूक", "तलवार", "फेंकना", "जमीन", "गोली", "लोहा", "शस्त्र"],
        "usage_notes": "युद्धक्षेत्रीय शस्त्र त्याग से उपजा राजनीतिक व मनोवैज्ञानिक मुहावरा।"
    },

    # ──────────────────────────────────────────────────────────────────────────
    # MARATHI IDIOMS / वाक्प्रचार (36 CANONICAL EXPRESSIONS)
    # ──────────────────────────────────────────────────────────────────────────
    "डोळ्यात धूळ फेकणे": {
        "canonical_concept": "deceive_someone",
        "language": "mr",
        "phrase": "डोळ्यात धूळ फेकणे",
        "idiom": "डोळ्यात धूळ फेकणे",
        "aliases": ["डोळ्यात धूळ फेकणे", "डोळ्यात धूळ फेकून", "डोळ्यात धूळ फेकली", "डोळ्यांत धूळ फेकणे", "डोळ्यात धूळ", "डोळ्यांत धूळ"],
        "meaning": "फसवणूक करणे किंवा चकवून पसार होणे (To deceive or pull wool over someone's eyes).",
        "example": "चोर पोलिसांच्या डोळ्यात धूळ फेकून अंधारात पसार झाला.",
        "category": "Deception & Crime",
        "idiomatic_keywords": ["फसवणूक", "चकवा", "चोर", "पसार", "विश्वासघात", "लबाडी", "कपट", "पोलिस"],
        "literal_keywords": ["डोळा", "धूळ", "माती", "फेकणे", "वारा", "डोळे", "पापणी", "चोळणे"],
        "usage_notes": "फसवेगिरी करून निसटून जाण्याच्या संदर्भातील पारंपरिक मराठी वाक्प्रचार."
    },
    "हात देणे": {
        "canonical_concept": "lending_hand",
        "language": "mr",
        "phrase": "हात देणे",
        "idiom": "हात देणे",
        "aliases": ["हात देणे", "हात दिला", "हात देत आहे", "हात द्यावा"],
        "meaning": "मदत करणे किंवा साहाय्य करणे (To lend a helping hand / assist someone).",
        "example": "संकटकाळात शेजाऱ्यांनी पुढे येऊन गरीब कुटुंबाला हात दिला.",
        "category": "Support & Kindness",
        "idiomatic_keywords": ["मदत", "साहाय्य", "संकट", "सहकार्य", "उपकार", "आधार", "कुटुंब", "शेजारी"],
        "literal_keywords": ["हात", "हथेली", "बोट", "स्पर्श", "पकडणे", "उंचवणे", "ओढणे", "शरीर"],
        "usage_notes": "अडीअडचणीत दुसऱ्याच्या साहाय्यासाठी धावून येण्याचा उदात्त भाव व्यक्त करतो."
    },
    "नाकी नऊ येणे": {
        "canonical_concept": "exhausted_distressed",
        "language": "mr",
        "phrase": "नाकी नऊ येणे",
        "idiom": "नाकी नऊ येणे",
        "aliases": ["नाकी नऊ येणे", "नाकी नऊ आले", "नाकी नऊ आणले", "नाकी नऊ येतात"],
        "meaning": "अतिशय त्रास होणे किंवा दमून बेजार होणे (To be utterly exhausted, harassed, or exasperated).",
        "example": "दुपारच्या कडक उन्हात डोंगर चढताना पर्यटकांच्या नाकी नऊ आले.",
        "category": "Fatigue & Distress",
        "idiomatic_keywords": ["त्रास", "बेजार", "थकवा", "कष्ट", "दमणूक", "हैराण", "डोंगर", "उकाडा"],
        "literal_keywords": ["नाक", "नऊ", "श्वास", "चेहरा", "संख्या", "गणना", "आकडे"],
        "usage_notes": "शरीर आणि मनाची पराकोटीची दमछाक दर्शवणारा अस्सल मराठी वाक्प्रचार."
    },
    "कान भरणे": {
        "canonical_concept": "poisoning_ears",
        "language": "mr",
        "phrase": "कान भरणे",
        "idiom": "कान भरणे",
        "aliases": ["कान भरणे", "कान भरले", "कान भरत होता", "कान भरले होते"],
        "meaning": "एखाद्याविरुद्ध चहाडी करणे किंवा मनात विष कालवणे (To poison someone's ears with gossip).",
        "example": "सावत्र भावाविरुद्ध कान भरून त्याने घरात भांडण लावून दिले.",
        "category": "Deception & Conflict",
        "idiomatic_keywords": ["चहाडी", "भांडण", "कलह", "गैरसमज", "कागाळी", "द्वेष", "चुगली", "मन"],
        "literal_keywords": ["कान", "पाणी", "कापूस", "थेंब", "मैल", "ऐकणे", "दवा", "छिद्र"],
        "usage_notes": "घरातील किंवा कामातील नातेसंबंध बिघडवण्यासाठी केलेल्या गुप्त कुरापती दर्शवतो."
    },
    "पाणी पाजणे": {
        "canonical_concept": "defeat_humiliate",
        "language": "mr",
        "phrase": "पाणी पाजणे",
        "idiom": "पाणी पाजणे",
        "aliases": ["पाणी पाजणे", "पाणी पाजले", "पाणी पाजणार", "पाणी पाजले होते"],
        "meaning": "सडेतोड पराभव करणे किंवा अद्दल घडवणे (To defeat decisively or teach a stern lesson).",
        "example": "शिवरायांच्या मावळ्यांनी गनिमी काव्याने शत्रूच्या प्रचंड फौजेला पाणी पाजले.",
        "category": "Victory & Defeat",
        "idiomatic_keywords": ["पराभव", "मावळे", "शत्रू", "धडा", "लढाई", "विजय", "गनिमी", "फौज"],
        "literal_keywords": ["पाणी", "ग्लास", "पिणे", "तहान", "पाजणे", "नळ", "भांडे", "विहीर"],
        "usage_notes": "मराठी इतिहासातील शौर्य आणि प्रतिपक्षाला चीत करण्याच्या पराक्रमाशी निगडित."
    },
    "पाठीशी घालणे": {
        "canonical_concept": "shield_protect",
        "language": "mr",
        "phrase": "पाठीशी घालणे",
        "idiom": "पाठीशी घालणे",
        "aliases": ["पाठीशी घालणे", "पाठीशी घातले", "पाठीशी घालत आहे", "पाठीशी घालतात"],
        "meaning": "संरक्षण देणे किंवा चुका लपवून पाठीराखण करणे (To shield, protect, or patronize).",
        "example": "मुलाच्या खोड्या माहीत असूनही आई नेहमी त्याला पाठीशी घालत असे.",
        "category": "Protection & Bias",
        "idiomatic_keywords": ["संरक्षण", "पाठराखण", "बचाव", "चूक", "समर्थन", "आई", "लाड", "आश्रय"],
        "literal_keywords": ["पाठ", "घालणे", "पाठीवर", "शरीर", "स्पर्श", "मागे", "उभे"],
        "usage_notes": "वात्सल्यातून किंवा पक्षपातातून एखाद्याचे दोष झाकण्याच्या प्रवृत्तीवर वापरला जातो."
    },
    "तोंडचे पाणी पळणे": {
        "canonical_concept": "petrified_with_fear",
        "language": "mr",
        "phrase": "तोंडचे पाणी पळणे",
        "idiom": "तोंडचे पाणी पळणे",
        "aliases": ["तोंडचे पाणी पळणे", "तोंडचे पाणी पळाले", "तोंडाचे पाणी पळाले"],
        "meaning": "भीतीने चेहरा पांढरा पडणे किंवा प्रचंड घाबरणे (To turn pale with sudden petrifying terror).",
        "example": "रात्री जंगलात अचानक वाघाची डरकाळी ऐकताच पर्यटकांच्या तोंडचे पाणी पळाले.",
        "category": "Emotion & Fear",
        "idiomatic_keywords": ["भीती", "घाबरणे", "थरकाप", "वाघ", "स्तब्ध", "धक्का", "धडकी", "घाबरगुंडी"],
        "literal_keywords": ["तोंड", "पाणी", "लाळ", "ओठ", "पळणे", "पिणे", "गळा", "धुणे"],
        "usage_notes": "अकल्पित संकटाने चेहऱ्यावरची टवटवी उडून जाण्याच्या जैविक प्रतिक्रियेचे वर्णन."
    },
    "कंबर कसणे": {
        "canonical_concept": "gird_loins",
        "language": "mr",
        "phrase": "कंबर कसणे",
        "idiom": "कंबर कसणे",
        "aliases": ["कंबर कसणे", "कंबर कसली", "कंबर कसून", "कंबर कसावी"],
        "meaning": "दृढनिश्चयाने कामाला लागणे किंवा तयारी करणे (To gird one's loins / resolve firmly to work).",
        "example": "दुष्काळावर मात करण्यासाठी ग्रामस्थांनी श्रमदानासाठी कंबर कसली.",
        "category": "Effort & Determination",
        "idiomatic_keywords": ["तयारी", "निश्चय", "श्रमदान", "परिश्रम", "सज्ज", "कार्य", "संकल्प", "प्रयत्न"],
        "literal_keywords": ["कंबर", "पट्टा", "धोतर", "कसणे", "बांधणे", "शरीर", "वेदना", "माकडहाड"],
        "usage_notes": "कठिण श्रमापूर्वी कपडे घट्ट बांधण्याच्या कृतीवरून जिद्दीचे प्रतीक."
    },
    "दगडावरची रेघ": {
        "canonical_concept": "carved_in_stone",
        "language": "mr",
        "phrase": "दगडावरची रेघ",
        "idiom": "दगडावरची रेघ",
        "aliases": ["दगडावरची रेघ", "दगडावरची रेघ ठरली"],
        "meaning": "कधीही न बदलणारा शब्द किंवा पक्का निर्णय (Something permanently fixed; carved in stone).",
        "example": "आबासाहेबांचे वचन म्हणजे गावातल्या प्रत्येकासाठी दगडावरची रेघ असते.",
        "category": "Truth & Permanence",
        "idiomatic_keywords": ["वचन", "निर्णय", "कायम", "अढळ", "सत्य", "नियम", "प्रामाणिक", "विश्वास"],
        "literal_keywords": ["दगड", "रेघ", "खडू", "छिन्नी", "शिलालेख", "ओढणे", "पाषाण", "खडक"],
        "usage_notes": "शिलालेखावरील अक्षरांप्रमाणे न पुसल्या जाणाऱ्या शब्दाची खात्री."
    },
    "उखळ पांढरे होणे": {
        "canonical_concept": "making_easy_fortune",
        "language": "mr",
        "phrase": "उखळ पांढरे होणे",
        "idiom": "उखळ पांढरे होणे",
        "aliases": ["उखळ पांढरे होणे", "उखळ पांढरे झाले", "उखळ पांढरे करून घेतले"],
        "meaning": "विपुल संपत्ती मिळणे किंवा भरपूर नफा होणे (To gain enormous windfall wealth or profit).",
        "example": "जमीन रिलायन्स प्रकल्पात विकल्यामुळे त्या शेतकऱ्याचे उखळ पांढरे झाले.",
        "category": "Wealth & Fortune",
        "idiomatic_keywords": ["संपत्ती", "नफा", "श्रीमंती", "पैसा", "भरभराट", "जमीन", "दौलत", "फायदा"],
        "literal_keywords": ["उखळ", "मुसळ", "पांढरे", "धान्य", "कांडणे", "तांदूळ", "दगडी", "रंग"],
        "usage_notes": "धान्य कांडताना उखळ तांदळाच्या पिठाने पांढरे होण्यावरून सुबत्तेचे रूपक."
    },
    "अंगाची लाही लाही होणे": {
        "canonical_concept": "furious_or_scorched",
        "language": "mr",
        "phrase": "अंगाची लाही लाही होणे",
        "idiom": "अंगाची लाही लाही होणे",
        "aliases": ["अंगाची लाही लाही होणे", "अंगाची लाही लाही झाली", "अंगाची लाही लाही होत होती"],
        "meaning": "संतापाने किंवा तीव्र उन्हाने प्रचंड अस्वस्थ होणे (To burn with rage or sweltering heat).",
        "example": "अपमानास्पद भाषण ऐकून स्वाभिमानी वक्त्याच्या अंगाची लाही लाही झाली.",
        "category": "Emotion & Anger",
        "idiomatic_keywords": ["संताप", "क्रोध", "अपमान", "तिळपापड", "चीड", "उष्णता", "आक्रोश", "क्षोभ"],
        "literal_keywords": ["अंग", "लाही", "ज्वारी", "भाजणे", "भट्टी", "उष्णता", "तवा", "दाणे"],
        "usage_notes": "भट्टीत फुटणाऱ्या लाह्यांप्रमाणे अंगात उसळणाऱ्या संतापाची अवस्था."
    },
    "उंटावरून शेळ्या हाकणे": {
        "canonical_concept": "armchair_advising",
        "language": "mr",
        "phrase": "उंटावरून शेळ्या हाकणे",
        "idiom": "उंटावरून शेळ्या हाकणे",
        "aliases": ["उंटावरून शेळ्या हाकणे", "उंटावरून शेळ्या हाकतात", "उंटावरून शेळ्या हाकल्या"],
        "meaning": "प्रत्यक्ष कोणतेही कष्ट न करता दूर बसून नुसते सल्ले देणे (Armchair advising without doing actual work).",
        "example": "शेतात घाम गाळणाऱ्यांना कार्यालयात बसून उंटावरून शेळ्या हाकणाऱ्यांनी शिकवू नये.",
        "category": "Work & Pretension",
        "idiomatic_keywords": ["सल्ला", "ऐदी", "दिखावा", "दूर", "अहंकार", "कष्ट", "श्रम", "कार्यालय"],
        "literal_keywords": ["उंट", "शेळी", "मेंढी", "हाकणे", "काठी", "वाळवंट", "कुरण", "चरणे"],
        "usage_notes": "उंटावर बसून जमिनीवरच्या शेळ्या हाकण्याच्या निरुपयोगी प्रयत्नावरून उपहासात्मक म्हणी/वाक्प्रचार."
    },
    "काखा वर करणे": {
        "canonical_concept": "helpless_shrug",
        "language": "mr",
        "phrase": "काखा वर करणे",
        "idiom": "काखा वर करणे",
        "aliases": ["काखा वर करणे", "काखा वर केल्या", "काखा वर करतो"],
        "meaning": "असमर्थता दर्शवणे किंवा हात झटकून मोकळे होणे (To shrug helplessly or feign complete ignorance).",
        "example": "पैशांची मागणी करताच कर्जदाराने सहजपणे काखा वर केल्या.",
        "category": "Refusal & Helplessness",
        "idiomatic_keywords": ["असमर्थ", "नकार", "हात", "पैसे", "कर्ज", "टाळाटाळ", "अडचण", "मोकळे"],
        "literal_keywords": ["काख", "हात", "वर", "शरीर", "उंचवणे", "कसरत", "बगले"],
        "usage_notes": "माझ्याकडे काहीच नाही असे दाखवण्यासाठी दोन्ही हात वर करण्याच्या मुद्रेवरून."
    },
    "कानावर हात ठेवणे": {
        "canonical_concept": "deny_all_knowledge",
        "language": "mr",
        "phrase": "कानावर हात ठेवणे",
        "idiom": "कानावर हात ठेवणे",
        "aliases": ["कानावर हात ठेवणे", "कानावर हात ठेवले", "कानावर हात ठेवतात"],
        "meaning": "काहीही ठाऊक नसल्याचे भासवून जबाबदारी झटकणे (To feign complete ignorance of an event).",
        "example": "घोटाळा उघडकीस येताच अधिकाऱ्यांनी कानावर हात ठेवले.",
        "category": "Deception & Evading",
        "idiomatic_keywords": ["अज्ञानाचा", "कांगावा", "झटकणे", "घोटाळा", "जबाबदारी", "टाळणे", "नाकबूल", "दोष"],
        "literal_keywords": ["कान", "हात", "ठेवणे", "ऐकणे", "आवाज", "बहिरा", "बोट"],
        "usage_notes": "मी काही ऐकलेच नाही असा आव आणून चौकशीपासून पळ काढणे."
    },
    "खडे फोडणे": {
        "canonical_concept": "criticize_fault_finding",
        "language": "mr",
        "phrase": "खडे फोडणे",
        "idiom": "खडे फोडणे",
        "aliases": ["खडे फोडणे", "खडे फोडत बसले", "खडे फोडतात", "खडे फोडले"],
        "meaning": "दुसऱ्याला अखंड दोष देणे किंवा टीका करत बसणे (To constantly find fault and grumble).",
        "example": "स्वतः काही न करता सरकारवर खडे फोडण्यात काही अर्थ नाही.",
        "category": "Criticism & Fault",
        "idiomatic_keywords": ["दोष", "टीका", "निंदा", "तक्रार", "नकारात्मक", "कुरबूर", "सरकार", "आरोप"],
        "literal_keywords": ["खडे", "दगड", "हातोडा", "फोडणे", "रस्ता", "मजूर", "खाण", "कण"],
        "usage_notes": "रस्त्यावर खडी फोडणाऱ्या मजुराच्या सततच्या हातोड्याप्रमाणे अखंड दोषारोप करणे."
    },
    "गळ्यात पडणे": {
        "canonical_concept": "thrusting_burden",
        "language": "mr",
        "phrase": "गळ्यात पडणे",
        "idiom": "गळ्यात पडणे",
        "aliases": ["गळ्यात पडणे", "गळ्यात पडले", "गळ्यात पडत आहे"],
        "meaning": "नको असलेली जबाबदारी बळजबरीने माथी मारली जाणे (To have an unwelcome burden thrust upon oneself).",
        "example": "मित्राने अर्धवट सोडलेला प्रकल्प अखेर माझ्याच गळ्यात पडला.",
        "category": "Burden & Responsibility",
        "idiomatic_keywords": ["जबाबदारी", "ओझे", "प्रकल्प", "नकोसा", "माथी", "काम", "बळजबरी", "अडचण"],
        "literal_keywords": ["गळा", "हार", "पडणे", "दोरी", "हात", "मिठी", "मान"],
        "usage_notes": "अवांछित भार अथवा व्यक्ती स्वतःच्या अंगावर येऊन आदळणे."
    },
    "घोडे पेंड खाणे": {
        "canonical_concept": "progress_stalled",
        "language": "mr",
        "phrase": "घोडे पेंड खाणे",
        "idiom": "घोडे पेंड खाणे",
        "aliases": ["घोडे पेंड खाणे", "घोडे पेंड खात आहे", "घोडे पेंड खात बसले"],
        "meaning": "एखादे काम ऐन मोक्याच्या क्षणी अडकून पडणे किंवा रेंगाळणे (Work gets unexpectedly stalled at a crucial stage).",
        "example": "इमारतीचे बांधकाम पूर्ण झाले, पण महापालिकेच्या मंजुरीत घोडे पेंड खात आहे.",
        "category": "Delay & Obstacle",
        "idiomatic_keywords": ["अडकले", "रेंगाळणे", "विलंब", "मंजुरी", "अडचण", "काम", "प्रकल्प", "थबकणे"],
        "literal_keywords": ["घोडा", "पेंड", "खाणे", "तबेला", "चारा", "पशु", "खोगीर", "रपेट"],
        "usage_notes": "धावणाऱ्या घोड्याने अचानक थांबून पेंड खाण्यास सुरुवात केल्यासारखी कामाची गती मंदावणे."
    },
    "चार हात लांब राहणे": {
        "canonical_concept": "keep_at_bay",
        "language": "mr",
        "phrase": "चार हात लांब राहणे",
        "idiom": "चार हात लांब राहणे",
        "aliases": ["चार हात लांब राहणे", "चार हात लांब राहतो", "चार हात लांब राहावे"],
        "meaning": "धोकादायक किंवा लबाड माणसापासून सुरक्षित अंतर ठेवणे (To keep someone at a safe distance / arm's length).",
        "example": "त्या भांडखोर शेजाऱ्यापासून चार हात लांब राहिलेलेच बरे.",
        "category": "Caution & Distance",
        "idiomatic_keywords": ["अंतर", "सावध", "दूर", "भांडखोर", "सुरक्षित", "टाळणे", "शांतता", "नकोसा"],
        "literal_keywords": ["चार", "हात", "लांब", "अंतर", "मोजणे", "मीटर", "पावले"],
        "usage_notes": "उपद्रवी माणसाच्या संपर्कात न येण्याचा व्यावहारिक शहाणपणा."
    },
    "जीव टांगणीला लागणे": {
        "canonical_concept": "extreme_anxiety",
        "language": "mr",
        "phrase": "जीव टांगणीला लागणे",
        "idiom": "जीव टांगणीला लागणे",
        "aliases": ["जीव टांगणीला लागणे", "जीव टांगणीला लागला", "जीव टांगणीला लागला होता"],
        "meaning": "प्रचंड काळजी किंवा चिंतेने मन अतिशय व्याकूळ होणे (To be in a state of agonizing anxiety / on tenterhooks).",
        "example": "मुलगा रात्री उशिरापर्यंत घरी न आल्यामुळे आईचा जीव टांगणीला लागला.",
        "category": "Emotion & Anxiety",
        "idiomatic_keywords": ["चिंता", "काळजी", "व्याकूळ", "धडधड", "आई", "उशीर", "भीती", "अस्वस्थ"],
        "literal_keywords": ["जीव", "टांगणे", "दोरी", "खिळा", "टांगणी", "फाशी", "हवा"],
        "usage_notes": "अनिश्चिततेच्या भीषण दबावाखाली मनाला होणाऱ्या यातनांचे चित्र."
    },
    "झाकले माणिक": {
        "canonical_concept": "hidden_gem",
        "language": "mr",
        "phrase": "झाकले माणिक",
        "idiom": "झाकले माणिक",
        "aliases": ["झाकले माणिक"],
        "meaning": "साध्या दिसणाऱ्या व्यक्तीमध्ये असलेला असाधारण सुप्त गुण (A hidden gem; modest person of immense talent).",
        "example": "शांत स्वभावाचा हा मुलगा गणितात इतका हुशार निघेल, हे झाकले माणिकच ठरले.",
        "category": "Talent & Modesty",
        "idiomatic_keywords": ["हुशार", "गुणवान", "साधेपणा", "रत्न", "प्रतिभा", "असामान्य", "आश्चर्य", "गणित"],
        "literal_keywords": ["माणिक", "रत्न", "कापड", "डबी", "झाकणे", "दागिना", "खाण"],
        "usage_notes": "बाहेरून प्रसिद्धी न मिळवता आतून अत्यंत तेजस्वी असणाऱ्या गुणी व्यक्तीचे वर्णन."
    },
    "डोळे उघडणे": {
        "canonical_concept": "eye_opener",
        "language": "mr",
        "phrase": "डोळे उघडणे",
        "idiom": "डोळे उघडणे",
        "aliases": ["डोळे उघडणे", "डोळे उघडले", "डोळे उघडावे लागतील"],
        "meaning": "सत्य परिस्थिती लक्षात येणे किंवा भ्रमाचा भोपळा फुटणे (To realize the harsh truth / have eyes opened).",
        "example": "व्यवसायात मोठा फटका बसल्यावर त्याचे डोळे उघडले.",
        "category": "Realization & Wisdom",
        "idiomatic_keywords": ["सत्य", "जाणीव", "भ्रमनिरास", "शहाणपण", "नुकसान", "अनुभव", "जागृती", "धडा"],
        "literal_keywords": ["डोळे", "उघडणे", "झाकणे", "झोप", "पापणी", "दृष्टी", "सकाळ"],
        "usage_notes": "अज्ञानातून किंवा भ्रमातून बाहेर येऊन वास्तवाचा स्वीकार करणे."
    },
    "नाक मुरडणे": {
        "canonical_concept": "turn_up_nose",
        "language": "mr",
        "phrase": "नाक मुरडणे",
        "idiom": "नाक मुरडणे",
        "aliases": ["नाक मुरडणे", "नाक मुरडले", "नाक मुरडत होती", "नाक मुरडतात"],
        "meaning": "नापसंती दर्शवणे किंवा एखाद्या गोष्टीला तुच्छ लेखणे (To turn up one's nose / show disdain).",
        "example": "आईने केलेल्या साध्या जेवणावर मुलाने लगेच नाक मुरडले.",
        "category": "Disdain & Disapproval",
        "idiomatic_keywords": ["नापसंती", "तुच्छ", "असमाधान", "नखरे", "चेहरा", "अनादर", "जेवण", "राग"],
        "literal_keywords": ["नाक", "मुरडणे", "हात", "चेहरा", "श्वास", "वास", "नाकपुडी"],
        "usage_notes": "अनादर किंवा नाराजी व्यक्त करताना चेहऱ्यावर येणाऱ्या स्वाभाविक आविर्भावावरून."
    },
    "पाय जमिनीवर असणे": {
        "canonical_concept": "down_to_earth",
        "language": "mr",
        "phrase": "पाय जमिनीवर असणे",
        "idiom": "पाय जमिनीवर असणे",
        "aliases": ["पाय जमिनीवर असणे", "पाय जमिनीवर आहेत", "पाय जमिनीवर राहिले पाहिजेत"],
        "meaning": "अफाट यश मिळूनही नम्र आणि वास्तववादी राहणे (To remain humble and grounded despite success).",
        "example": "इतका मोठा उद्योगपती असूनही त्याचे पाय अजूनही जमिनीवर आहेत.",
        "category": "Humility & Character",
        "idiomatic_keywords": ["नम्र", "वास्तव", "उद्योगपती", "अहंकाररहित", "यश", "साधेपणा", "संस्कार", "मोठेपण"],
        "literal_keywords": ["पाय", "जमीन", "माती", "उभे", "चालणे", "उड्या", "तळपाय"],
        "usage_notes": "यशाच्या मदाने हवेत न उडता नम्रतेने पाय मातीत रोवून राहण्याची वृत्ती."
    },
    "पाठीवर हात फिरवणे": {
        "canonical_concept": "pat_on_back",
        "language": "mr",
        "phrase": "पाठीवर हात फिरवणे",
        "idiom": "पाठीवर हात फिरवणे",
        "aliases": ["पाठीवर हात फिरवणे", "पाठीवर हात फिरवला", "पाठीवर हात फिरवून"],
        "meaning": "कौतुक करणे, धीर देणे किंवा शाबासकी देणे (To comfort, encourage, or give a warm pat on back).",
        "example": "दुःखात खचलेल्या मित्राच्या पाठीवर हात फिरवून त्याने धीर दिला.",
        "category": "Encouragement & Comfort",
        "idiomatic_keywords": ["धीर", "शाबासकी", "कौतुक", "सांत्वन", "मदत", "मित्र", "प्रेम", "उत्साह"],
        "literal_keywords": ["पाठ", "हात", "फिरवणे", "स्पर्श", "शरीर", "कंधा", "मागे"],
        "usage_notes": "संवेदनशील स्पर्शामधून आपुलकी आणि मानसिक आधार देण्याची कृती."
    },
    "पोटात कावळे ओरडणे": {
        "canonical_concept": "ravenous_hunger",
        "language": "mr",
        "phrase": "पोटात कावळे ओरडणे",
        "idiom": "पोटात कावळे ओरडणे",
        "aliases": ["पोटात कावळे ओरडणे", "पोटात कावळे ओरडत आहेत", "पोटात कावळे ओरडू लागले"],
        "meaning": "अतिशय तीव्र भूक लागणे (To be ravenously hungry / have one's stomach growling).",
        "example": "सकाळपासून उपाशी असल्यामुळे दुपारी पोटात कावळे ओरडू लागले.",
        "category": "Hunger & Sensation",
        "idiomatic_keywords": ["भूक", "उपाशी", "जेवण", "अन्न", "दुपार", "तहान", "कळवळणे", "गती"],
        "literal_keywords": ["पोट", "कावळा", "ओरडणे", "पक्षी", "झाड", "आवाज", "काव-काव"],
        "usage_notes": "भुकेमुळे पोटातील जठरातून येणाऱ्या आवाजाची कावळ्यांच्या ओरडण्याशी केलेली विनोदी तुलना."
    },
    "बारा गावचे पाणी पिणे": {
        "canonical_concept": "worldly_wise",
        "language": "mr",
        "phrase": "बारा गावचे पाणी पिणे",
        "idiom": "बारा गावचे पाणी पिणे",
        "aliases": ["बारा गावचे पाणी पिणे", "बारा गावचे पाणी प्यायलेला", "बारा गावचे पाणी पिऊन आला"],
        "meaning": "अफाट अनुभव असणे किंवा जग फिरून धूर्त/हुशार बनणे (To be worldly-wise, deeply experienced).",
        "example": "त्या वकिलाला फसवणे सोपे नाही, त्याने बारा गावचे पाणी प्यायले आहे.",
        "category": "Wisdom & Experience",
        "idiomatic_keywords": ["अनुभवी", "हुशार", "धूर्त", "जग", "वकील", "ज्ञान", "शहाणा", "कौशल्य"],
        "literal_keywords": ["बारा", "गाव", "पाणी", "पिणे", "विहीर", "नदी", "प्रवास", "घोट"],
        "usage_notes": "अनेक प्रदेशांतील समाज आणि संस्कृती जवळून अनुभवलेल्या चाणाक्ष माणसाचे वर्णन."
    },
    "मुठीत असणे": {
        "canonical_concept": "under_thumb",
        "language": "mr",
        "phrase": "मुठीत असणे",
        "idiom": "मुठीत असणे",
        "aliases": ["मुठीत असणे", "मुठीत ठेवणे", "मुठीत ठेवला आहे", "मुठीत असतात"],
        "meaning": "पूर्णपणे ताब्यात किंवा प्रभावाखाली असणे (To be completely under someone's control/thumb).",
        "example": "आपल्या हुशारीच्या जोरावर त्याने संपूर्ण संघटनेला मुठीत ठेवले आहे.",
        "category": "Control & Influence",
        "idiomatic_keywords": ["ताबा", "नियंत्रण", "प्रभाव", "संघटना", "अधिकार", "दबाव", "हुकूमत", "अधिपत्य"],
        "literal_keywords": ["मूठ", "बोटे", "हात", "पकड", "बंद", "हथेली", "नाणे"],
        "usage_notes": "एखाद्या व्यक्तीला किंवा समूहाला मुठीतल्या वस्तूंप्रमाणे इच्छेनुरूप चालवणे."
    },
    "रक्ताचे पाणी करणे": {
        "canonical_concept": "burn_the_midnight_oil",
        "language": "mr",
        "phrase": "रक्ताचे पाणी करणे",
        "idiom": "रक्ताचे पाणी करणे",
        "aliases": ["रक्ताचे पाणी करणे", "रक्ताचे पाणी केले", "रक्ताचे पाणी करून"],
        "meaning": "अतोनात व पराकोटीचे शारीरिक/मानसिक कष्ट उपसणे (To toil with every ounce of sweat and blood).",
        "example": "शेतकऱ्याने रक्ताचे पाणी करून शेतात सोन्यासारखे पीक पिकवले.",
        "category": "Effort & Hard Work",
        "idiomatic_keywords": ["कष्ट", "शेतकरी", "शेत", "शेती", "परिश्रम", "घाम", "पीक", "मेहनत", "साधना", "जिद्द", "सोन्यासारखे"],
        "literal_keywords": ["रक्त", "पाणी", "वाहणे", "लाल", "थेंब", "शीरा", "नदी"],
        "usage_notes": "शरीरातील रक्ताचे रूपांतर घामाच्या पाण्यात होईपर्यंत केलेल्या श्रमाचे भव्य प्रतीक."
    },
    "वाटाण्याच्या अक्षता लावणे": {
        "canonical_concept": "flat_refusal",
        "language": "mr",
        "phrase": "वाटाण्याच्या अक्षता लावणे",
        "idiom": "वाटाण्याच्या अक्षता लावणे",
        "aliases": ["वाटाण्याच्या अक्षता लावणे", "वाटाण्याच्या अक्षता लावल्या", "वाटाण्याच्या अक्षता लावून"],
        "meaning": "स्पष्ट शब्दांत किंवा कोरड्यापणे नकार देणे (To reject flatly or refuse assistance coldly).",
        "example": "मदतीची याचना घेऊन गेलेल्या नातेवाईकांना श्रीमंत काकांनी वाटाण्याच्या अक्षता लावल्या.",
        "category": "Refusal & Coldness",
        "idiomatic_keywords": ["नकार", "मना", "कोरडेपणा", "इनकार", "काका", "मदत", "अपमान", "निराशा"],
        "literal_keywords": ["वाटाणा", "अक्षता", "तांदूळ", "लग्न", "कपाळ", "पूजा", "दाणे"],
        "usage_notes": "शुभकार्यातील अक्षतांऐवजी वाटाणे फेकण्यासारखा निरुत्साही व उर्मट नकार."
    },
    "हात चोळणे": {
        "canonical_concept": "wring_hands_regret",
        "language": "mr",
        "phrase": "हात चोळणे",
        "idiom": "हात चोळणे",
        "aliases": ["हात चोळणे", "हात चोळत बसले", "हात चोळावे लागले"],
        "meaning": "संधी निसटून गेल्यावर हताश होऊन पश्चात्ताप करणे (To wring hands in helpless regret).",
        "example": "वेळेत अर्ज न केल्यामुळे नोकरीची सुवर्णसंधी गमावून तो हात चोळत बसला.",
        "category": "Regret & Lost Chance",
        "idiomatic_keywords": ["पश्चात्ताप", "हताश", "संधी", "खंत", "उशीर", "नुकसान", "निराशा", "वेळ"],
        "literal_keywords": ["हात", "चोळणे", "हथेली", "थंडी", "घासणे", "तेल", "त्वचा"],
        "usage_notes": "वेळ निघून गेल्यावर केवळ हताशपणे तळहात एकमेकांवर घासण्याशिवाय काहीही न उरणे."
    },
    "हात टेकणे": {
        "canonical_concept": "admit_defeat",
        "language": "mr",
        "phrase": "हात टेकणे",
        "idiom": "हात टेकणे",
        "aliases": ["हात टेकणे", "हात टेकले", "हात टेकले होते"],
        "meaning": "नाइलाज होऊन माघार घेणे किंवा शरण येणे (To throw up one's hands / concede defeat).",
        "example": "रुग्णाचे आजारपण इतके वाढले की शेवटी डॉक्टरांनीही हात टेकले.",
        "category": "Defeat & Helplessness",
        "idiomatic_keywords": ["शरण", "माघार", "नाइलाज", "असमर्थ", "डॉक्टर", "हार", "थकले", "उपाय"],
        "literal_keywords": ["हात", "टेकणे", "जमीन", "टेबल", "तळहात", "उभे", "बसणे"],
        "usage_notes": "सर्व उपाय खुंटल्यावर जमिनीवर किंवा टेबलावर हात ठेवून लाचारी मान्य करणे."
    },
    "हुरूप येणे": {
        "canonical_concept": "fresh_enthusiasm",
        "language": "mr",
        "phrase": "हुरूप येणे",
        "idiom": "हुरूप येणे",
        "aliases": ["हुरूप येणे", "हुरूप आला", "हुरूप येतो"],
        "meaning": "नवा उत्साह, उमेद किंवा जोम निर्माण होणे (To feel a surge of fresh enthusiasm or energy).",
        "example": "शिक्षकांच्या शाबासकीमुळे विद्यार्थ्यांना अभ्यासाचा नवा हुरूप आला.",
        "category": "Energy & Enthusiasm",
        "idiomatic_keywords": ["उत्साह", "उमेद", "जोम", "प्रेरणा", "शाबासकी", "आनंद", "अभ्यास", "स्फूर्ती"],
        "literal_keywords": ["हुरूप", "हवा", "उष्णता", "शरीर", "मन", "कंपन"],
        "usage_notes": "प्रोत्साहनाने मानवी मनात भरून येणाऱ्या नवचैतन्याचा भाव."
    },
    "अस्मान दाखवणे": {
        "canonical_concept": "crush_opposition",
        "language": "mr",
        "phrase": "अस्मान दाखवणे",
        "idiom": "अस्मान दाखवणे",
        "aliases": ["अस्मान दाखवणे", "अस्मान दाखवले", "अस्मान दाखवीन"],
        "meaning": "कुस्तीत किंवा युद्धात प्रतिस्पर्ध्याला आस्मान दाखवून पूर्णपणे चीत करणे (To pin down and thoroughly crush opponent).",
        "example": "लाल मातीच्या आखाड्यात पठ्ठ्याने प्रतिस्पर्धी मल्लाला एका झटक्यात अस्मान दाखवले.",
        "category": "Victory & Wrestling",
        "idiomatic_keywords": ["आखाडा", "पैलवान", "कुस्ती", "पराभव", "मल्ल", "चीत", "शौर्य", "विजय"],
        "literal_keywords": ["अस्मान", "आकाश", "दाखवणे", "ढग", "तारे", "वर", "नजर"],
        "usage_notes": "कुस्तीच्या आखाड्यात प्रतिस्पर्ध्याची पाठ जमिनीला टेकवून वरचे आकाश दाखवण्याच्या डावावरून."
    },
    "गळ घालणे": {
        "canonical_concept": "persistent_pleading",
        "language": "mr",
        "phrase": "गळ घालणे",
        "idiom": "गळ घालणे",
        "aliases": ["गळ घालणे", "गळ घातली", "गळ घालत होता"],
        "meaning": "एखाद्या गोष्टीसाठी अतिशय हट्ट करणे किंवा अतोनात आग्रह धरणे (To plead or importune relentlessly).",
        "example": "गावी जाण्यासाठी मुलाने वडिलांना खूप गळ घातली.",
        "category": "Pleading & Persistence",
        "idiomatic_keywords": ["आग्रह", "हट्ट", "विनंती", "वडिल", "लाड", "हट्टास", "प्रवास", "मागणी"],
        "literal_keywords": ["गळ", "मासा", "गळफास", "घास", "दोरी", "पकडणे"],
        "usage_notes": "माशाच्या गळाप्रमाणे एखाद्याच्या निर्णयाला खिळवून ठेवणाऱ्या आग्रहावरून."
    },
    "तोंडात बोट घालणे": {
        "canonical_concept": "astonished_wonder",
        "language": "mr",
        "phrase": "तोंडात बोट घालणे",
        "idiom": "तोंडात बोट घालणे",
        "aliases": ["तोंडात बोट घालणे", "तोंडात बोट घातले", "तोंडात बोटे घालतील"],
        "meaning": "तीव्र आश्चर्याने थक्क होऊन जाणे (To be struck with speechless wonder / bite fingers in amazement).",
        "example": "सहा वर्षांच्या बालकाचे अद्भुत शास्त्रीय संगीत ऐकून श्रोत्यांनी तोंडात बोट घातले.",
        "category": "Wonder & Amazement",
        "idiomatic_keywords": ["आश्चर्य", "थक्क", "अद्भुत", "संगीत", "प्रतिभा", "चमत्कार", "दंग", "श्रोते"],
        "literal_keywords": ["तोंड", "बोट", "घालणे", "दात", "ओठ", "चावणे", "बालक"],
        "usage_notes": "अकल्पित आश्चर्य पाहिल्यावर व्यक्तीच्या चेहऱ्यावर उमटणारी उत्स्फूर्त शारीरिक मुद्रा."
    },
    "आभाळ फाटणे": {
        "canonical_concept": "catastrophic_calamity",
        "language": "mr",
        "phrase": "आभाळ फाटणे",
        "idiom": "आभाळ फाटणे",
        "aliases": ["आभाळ फाटणे", "आभाळ फाटले", "आभाळ फाटल्यासारखे"],
        "meaning": "सर्व बाजूंनी एकदम मोठे संकट कोसळणे किंवा दुःखाचा डोंगर कोसळणे (When all hell breaks loose / immense tragedy strikes).",
        "example": "महापुरात घर आणि शेती वाहून गेल्यामुळे त्या कुटुंबावर जणू आभाळच फाटले.",
        "category": "Misfortune & Tragedy",
        "idiomatic_keywords": ["संकट", "महापूर", "आपत्ती", "कुटुंब", "नुकसान", "असह्य", "वेदना", "सर्वनाश"],
        "literal_keywords": ["आभाळ", "आकाश", "फाटणे", "ढग", "पाऊस", "विजा", "तडाखा"],
        "usage_notes": "आकाशालाच भगदाड पडून सर्व संकटे एकदम अंगावर कोसळण्याच्या अतीव दुःखाची उपमा."
    }
}


def get_all_idioms(language=None):
    """
    Return list of canonical idiom strings.
    If language is None or 'all', returns all 108 idioms.
    If language is 'en', 'hi', or 'mr', filters accordingly.
    """
    if language is None or language == "all":
        return list(IDIOM_DICTIONARY.keys())
    return [k for k, v in IDIOM_DICTIONARY.items() if v.get("language") == language.lower()]


def get_idioms_by_language(language="en"):
    """
    Return dictionary subset filtered by language ('en', 'hi', 'mr').
    """
    lang_lower = language.lower() if language else "en"
    return {k: v for k, v in IDIOM_DICTIONARY.items() if v.get("language") == lang_lower}


def get_idiom_info(idiom_name, language=None):
    """
    Retrieve full metadata for a given canonical idiom or alias across languages.
    """
    if not idiom_name:
        return None
    normalized = unicodedata.normalize("NFC", idiom_name.strip())
    norm_lower = normalized.lower()

    # 1. Direct match
    if normalized in IDIOM_DICTIONARY:
        info = IDIOM_DICTIONARY[normalized]
        if language is None or info.get("language") == language.lower():
            return info

    if norm_lower in IDIOM_DICTIONARY:
        info = IDIOM_DICTIONARY[norm_lower]
        if language is None or info.get("language") == language.lower():
            return info

    # 2. Check aliases and phrase
    for key, info in IDIOM_DICTIONARY.items():
        if language is not None and info.get("language") != language.lower():
            continue
        if norm_lower == key.lower() or normalized == key:
            return info
        for alias in info.get("aliases", []):
            if normalized == alias or norm_lower == alias.lower():
                return info
            if unicodedata.normalize("NFC", alias) == normalized:
                return info

    # 3. Check by canonical concept
    for key, info in IDIOM_DICTIONARY.items():
        if info.get("canonical_concept") == idiom_name:
            if language is None or info.get("language") == language.lower():
                return info

    return None


def get_all_concepts():
    """Return sorted unique list of all canonical concepts."""
    concepts = set(v["canonical_concept"] for v in IDIOM_DICTIONARY.values())
    return sorted(list(concepts))


if __name__ == "__main__":
    print(f"Total idioms in knowledge base: {len(IDIOM_DICTIONARY)}")
    en_count = len(get_all_idioms('en'))
    hi_count = len(get_all_idioms('hi'))
    mr_count = len(get_all_idioms('mr'))
    print(f"English idioms: {en_count}")
    print(f"Hindi idioms:   {hi_count}")
    print(f"Marathi idioms: {mr_count}")
    print(f"Unique canonical concepts: {len(get_all_concepts())}")
