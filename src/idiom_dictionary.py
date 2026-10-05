"""
Idiom Dictionary and Knowledge Base
Contains canonical idiom metadata, definitions, examples, categories,
and context hints for contextual explanation generation.
"""

IDIOM_DICTIONARY = {
    "break the ice": {
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
        "idiom": "beat around the bush",
        "aliases": ["beat around the bush", "beats around the bush", "beating around the bush", "beat about the bush"],
        "meaning": "To discuss a topic ambiguously and avoid addressing the core issue directly.",
        "example": "Stop beating around the bush and tell me what the feedback really was.",
        "category": "Communication & Social",
        "idiomatic_keywords": ["direct", "avoid", "clear", "evasive", "hesitant", "honest", "frank", "point", "topic", "truth", "speak"],
        "literal_keywords": ["bush", "stick", "branches", "foliage", "hunting", "game", "garden", "trimming", "hedges", "forest"],
        "usage_notes": "Hunters in medieval times would beat shrubs to flush out birds before the main hunter aimed."
    },
    "blessing in disguise": {
        "idiom": "blessing in disguise",
        "aliases": ["blessing in disguise", "blessings in disguise"],
        "meaning": "An apparent misfortune or setback that eventually yields beneficial results.",
        "example": "Losing that entry-level job was a blessing in disguise because it led him to start his own startup.",
        "category": "Fortune & Outlook",
        "idiomatic_keywords": ["opportunity", "misfortune", "advantage", "benefit", "setback", "turned", "better", "eventually", "lucky", "startup"],
        "literal_keywords": ["costume", "disguise", "mask", "priest", "holy", "blessing", "ritual", "monk", "clothing", "appearance"],
        "usage_notes": "Philosophical concept highlighting how initial setbacks often pave the way for superior long-term outcomes."
    },
    "burn the midnight oil": {
        "idiom": "burn the midnight oil",
        "aliases": ["burn the midnight oil", "burning the midnight oil", "burned the midnight oil", "burns the midnight oil", "burnt the midnight oil"],
        "meaning": "To work or study late into the night.",
        "example": "Engineering students often burn the midnight oil before end-semester examinations.",
        "category": "Effort & Work",
        "idiomatic_keywords": ["study", "work", "night", "exam", "deadline", "project", "late", "effort", "assignment", "fatigue"],
        "literal_keywords": ["lamp", "oil", "flame", "kerosene", "fuel", "candle", "wick", "lantern", "burn", "lighting"],
        "usage_notes": "Originates from working by oil lamps before the widespread adoption of electrical lighting."
    },
    "call it a day": {
        "idiom": "call it a day",
        "aliases": ["call it a day", "called it a day", "calling it a day", "calls it a day"],
        "meaning": "To conclude a work session or temporarily halt an activity.",
        "example": "We have completed all debug tasks, so let's call it a day.",
        "category": "Effort & Work",
        "idiomatic_keywords": ["finish", "stop", "tired", "done", "wrap", "conclude", "session", "office", "pack", "rest", "complete"],
        "literal_keywords": ["daylight", "calendar", "referee", "game", "named", "hours", "schedule", "afternoon", "date"],
        "usage_notes": "Informal workplace idiom signaling agreement to cease professional work for the day."
    },
    "on cloud nine": {
        "idiom": "on cloud nine",
        "aliases": ["on cloud nine", "on cloud 9", "upon cloud nine"],
        "meaning": "Experiencing extreme happiness, joy, or euphoria.",
        "example": "After receiving the prestigious scholarship, she was on cloud nine.",
        "category": "Emotion & State",
        "idiomatic_keywords": ["happy", "joy", "excited", "elated", "scholarship", "victory", "celebration", "ecstatic", "thrilled", "proud"],
        "literal_keywords": ["cloud", "cumulonimbus", "altitude", "meteorology", "sky", "plane", "flying", "atmosphere", "nine"],
        "usage_notes": "Derived from the International Cloud Atlas classification where 'Cloud Nine' represented towering, puffy cumulonimbus clouds."
    },
    "pull someone's leg": {
        "idiom": "pull someone's leg",
        "aliases": ["pull someone's leg", "pull my leg", "pull your leg", "pull his leg", "pull her leg", "pulling my leg", "pulling your leg", "pulling his leg", "pulling her leg", "pulled my leg", "pulled his leg", "pulled her leg"],
        "meaning": "To tease or jokingly deceive someone in a lighthearted manner.",
        "example": "Don't get upset; he was only pulling your leg about the quiz.",
        "category": "Humor & Teasing",
        "idiomatic_keywords": ["joke", "kidding", "prank", "tease", "laugh", "fun", "believe", "serious", "playful", "tricked"],
        "literal_keywords": ["leg", "limb", "muscle", "physiotherapy", "tether", "rope", "trip", "bone", "pulling", "ankle"],
        "usage_notes": "Popularized in 19th-century street slang referring humorously to tripping someone playfully."
    },
    "raining cats and dogs": {
        "idiom": "raining cats and dogs",
        "aliases": ["raining cats and dogs", "rained cats and dogs", "rains cats and dogs"],
        "meaning": "Raining very heavily or experiencing a severe downpour.",
        "example": "We postponed the football tournament because it was raining cats and dogs.",
        "category": "Weather & Environment",
        "idiomatic_keywords": ["heavy", "downpour", "storm", "flood", "soaked", "monsoon", "torrential", "puddle", "umbrella", "postponed"],
        "literal_keywords": ["animals", "felines", "canines", "falling", "pets", "sky", "cartoon", "puppies", "kittens", "animation"],
        "usage_notes": "May stem from 17th-century England when heavy rain washed stray animals through town streets."
    },
    "a dime a dozen": {
        "idiom": "a dime a dozen",
        "aliases": ["a dime a dozen", "dime a dozen"],
        "meaning": "Very common, plentiful, and hence having little unique value.",
        "example": "Generic mobile applications are a dime a dozen in today's software market.",
        "category": "Cost & Value",
        "idiomatic_keywords": ["common", "plentiful", "generic", "everywhere", "ordinary", "unexceptional", "value", "abundant", "market"],
        "literal_keywords": ["coins", "dime", "cents", "dozen", "twelve", "currency", "eggs", "store", "price", "sale"],
        "usage_notes": "Originated in the US when items priced at a dime (10 cents) for twelve units indicated abundance."
    },
    "kill two birds with one stone": {
        "idiom": "kill two birds with one stone",
        "aliases": ["kill two birds with one stone", "killed two birds with one stone", "killing two birds with one stone", "kills two birds with one stone"],
        "meaning": "To achieve two distinct objectives through a single action.",
        "example": "By biking to work, he killed two birds with one stone: getting fit and saving money.",
        "category": "Efficiency & Action",
        "idiomatic_keywords": ["efficient", "dual", "accomplish", "solve", "multitask", "saving", "benefit", "smart", "strategy", "twofold"],
        "literal_keywords": ["birds", "stone", "slingshot", "hunter", "hunting", "target", "weapon", "feathers", "kill", "rock"],
        "usage_notes": "Proverb traceable back to Ovid and ancient Greek folklore depicting extraordinary efficiency."
    },
    "barking up the wrong tree": {
        "idiom": "barking up the wrong tree",
        "aliases": ["barking up the wrong tree", "barked up the wrong tree", "barks up the wrong tree", "bark up the wrong tree"],
        "meaning": "Pursuing a mistaken line of inquiry, reasoning, or accusation.",
        "example": "If you think I took your textbook, you are barking up the wrong tree.",
        "category": "Mistakes & Direction",
        "idiomatic_keywords": ["mistake", "wrong", "accusing", "misguided", "pursuing", "fault", "assumption", "direction", "investigation"],
        "literal_keywords": ["dog", "hound", "tree", "branches", "barking", "chasing", "squirrel", "canine", "forest", "woodland"],
        "usage_notes": "American hunting phrase where hunting hounds chased prey up trees and occasionally barked at empty trunks."
    },
    "elephant in the room": {
        "idiom": "elephant in the room",
        "aliases": ["elephant in the room", "the elephant in the room", "elephants in the room"],
        "meaning": "An obvious, major problem or controversial issue that everyone avoids addressing.",
        "example": "The budget deficit was the elephant in the room during the executive board meeting.",
        "category": "Conflict & Issues",
        "idiomatic_keywords": ["avoid", "unspoken", "obvious", "problem", "taboo", "ignoring", "awkward", "deficit", "board", "tension"],
        "literal_keywords": ["elephant", "safari", "zoo", "animal", "trunk", "room", "pachyderm", "mammal", "enclosure", "cage"],
        "usage_notes": "First referenced in 19th-century philosophical prose and popularized in modern corporate dialogue."
    },
    "best of both worlds": {
        "idiom": "best of both worlds",
        "aliases": ["best of both worlds", "the best of both worlds"],
        "meaning": "Enjoying the advantages of two distinctly different situations simultaneously.",
        "example": "Working remotely gives him the best of both worlds: good income and family time.",
        "category": "Opportunity & Balance",
        "idiomatic_keywords": ["balance", "advantage", "benefit", "convenience", "flexibility", "ideal", "situation", "compromise", "remote"],
        "literal_keywords": ["planets", "worlds", "travel", "globe", "continents", "earth", "universe", "destinations", "geography"],
        "usage_notes": "Emphasizes finding harmony between conflicting choices, such as city vs rural life or work vs leisure."
    },
    "add fuel to the fire": {
        "idiom": "add fuel to the fire",
        "aliases": ["add fuel to the fire", "added fuel to the fire", "adding fuel to the fire", "adds fuel to the fire"],
        "meaning": "To worsen an already intense, hostile, or difficult conflict.",
        "example": "His harsh response only added fuel to the fire during the union debate.",
        "category": "Conflict & Relations",
        "idiomatic_keywords": ["worsen", "escalate", "conflict", "anger", "argument", "hostility", "intense", "provoke", "irritate", "dispute"],
        "literal_keywords": ["fire", "wood", "gasoline", "fuel", "flames", "fireplace", "bonfire", "campfire", "combustion", "burn"],
        "usage_notes": "Ancient Roman metaphor recorded by Livy (oleum addere camino)."
    },
    "cut corners": {
        "idiom": "cut corners",
        "aliases": ["cut corners", "cutting corners", "cuts corners"],
        "meaning": "To do something hastily or cheaply by omitting essential standards or safety measures.",
        "example": "The contractor was penalized for cutting corners on the bridge construction materials.",
        "category": "Quality & Ethics",
        "idiomatic_keywords": ["cheap", "shoddy", "compromise", "quality", "safety", "fast", "careless", "regulations", "penalized", "standards"],
        "literal_keywords": ["corners", "scissors", "fabric", "wood", "angles", "carpentry", "square", "paper", "cutting", "geometric"],
        "usage_notes": "Originated from horse-drawn carriage drivers taking sharp turns across corners to shorten distance."
    },
    "get cold feet": {
        "idiom": "get cold feet",
        "aliases": ["get cold feet", "got cold feet", "getting cold feet", "gets cold feet", "have cold feet", "had cold feet"],
        "meaning": "To suddenly become nervous or hesitant about carrying out a planned significant action.",
        "example": "The entrepreneur got cold feet right before signing the venture acquisition deal.",
        "category": "Emotion & Hesitation",
        "idiomatic_keywords": ["nervous", "hesitant", "backed", "fear", "anxious", "wedding", "signing", "deal", "second", "thoughts", "retracted"],
        "literal_keywords": ["feet", "temperature", "winter", "socks", "cold", "snow", "toes", "ice", "shoes", "frostbite"],
        "usage_notes": "Literary origins suggest feet losing warmth when circulation drops due to acute fear or psychological stress."
    },
    "go the extra mile": {
        "idiom": "go the extra mile",
        "aliases": ["go the extra mile", "went the extra mile", "going the extra mile", "goes the extra mile"],
        "meaning": "To make a special effort beyond what is required to achieve success or help someone.",
        "example": "Our customer support team always goes the extra mile to resolve user issues.",
        "category": "Effort & Dedication",
        "idiomatic_keywords": ["effort", "dedication", "customer", "support", "exceed", "help", "committed", "standards", "exceptional", "care"],
        "literal_keywords": ["mile", "distance", "walking", "running", "marathon", "road", "kilometer", "track", "pavement", "travel"],
        "usage_notes": "Derived from Biblical references instructing followers to walk an additional mile when compelled."
    },
    "jump on the bandwagon": {
        "idiom": "jump on the bandwagon",
        "aliases": ["jump on the bandwagon", "jumped on the bandwagon", "jumping on the bandwagon", "jumps on the bandwagon"],
        "meaning": "To adopt a popular trend, opinion, or activity simply because many others are doing so.",
        "example": "Many companies jumped on the AI bandwagon to attract speculative venture capital.",
        "category": "Trends & Conformity",
        "idiomatic_keywords": ["trend", "popular", "hype", "follow", "adopt", "conform", "fashion", "crowd", "speculative", "fad"],
        "literal_keywords": ["bandwagon", "parade", "circus", "wagon", "musicians", "cart", "vehicle", "jump", "carnival", "wheels"],
        "usage_notes": "19th-century American political campaigns featured lively parade wagons carrying musicians to draw crowds."
    },
    "miss the boat": {
        "idiom": "miss the boat",
        "aliases": ["miss the boat", "missed the boat", "missing the boat", "misses the boat"],
        "meaning": "To lose an opportunity or chance by acting too slowly or hesitating.",
        "example": "Investors who hesitated to buy early shares completely missed the boat.",
        "category": "Opportunity & Timing",
        "idiomatic_keywords": ["opportunity", "late", "chance", "hesitated", "investors", "regret", "lost", "delay", "timing", "market"],
        "literal_keywords": ["boat", "ferry", "dock", "pier", "harbor", "ship", "water", "sailing", "passenger", "ticket"],
        "usage_notes": "Figurative phrase derived from travelers arriving late at harbor docks after passenger vessels departed."
    },
    "speak of the devil": {
        "idiom": "speak of the devil",
        "aliases": ["speak of the devil", "speaking of the devil", "speaks of the devil"],
        "meaning": "Acknowledging the sudden arrival of someone who was just being discussed.",
        "example": "We were just discussing Alex's promotion, and speak of the devil, here he comes.",
        "category": "Communication & Coincidence",
        "idiomatic_keywords": ["arrived", "mentioning", "talking", "enters", "coincidence", "walks", "timing", "discussing", "topic"],
        "literal_keywords": ["devil", "demon", "satan", "holy", "religious", "hell", "folklore", "evil", "priest", "curse"],
        "usage_notes": "Shortened form of the traditional English proverb 'Speak of the devil and he doth appear'."
    },
    "through thick and thin": {
        "idiom": "through thick and thin",
        "aliases": ["through thick and thin", "thick and thin"],
        "meaning": "Remaining steadfast, loyal, and supportive under all circumstances, good and bad.",
        "example": "They have been best friends through thick and thin for over twenty years.",
        "category": "Loyalty & Relationships",
        "idiomatic_keywords": ["loyal", "supportive", "adversity", "friendship", "partner", "hardship", "together", "devoted", "relationship", "years"],
        "literal_keywords": ["vegetation", "woods", "forest", "dense", "trees", "foliage", "thicket", "brush", "slender", "branches"],
        "usage_notes": "Originated from traversing dense (thick) and sparse (thin) woodland pathways in old English hunting."
    },
    "hit the sack": {
        "idiom": "hit the sack",
        "aliases": ["hit the sack", "hits the sack", "hitting the sack", "hit the hay"],
        "meaning": "To go to bed or fall asleep after a tiring day.",
        "example": "After a grueling twelve-hour shift, the nurse was ready to hit the sack.",
        "category": "Rest & Sleep",
        "idiomatic_keywords": ["sleep", "bed", "tired", "exhausted", "night", "rest", "fatigued", "shift", "slumber", "pillow"],
        "literal_keywords": ["sack", "bag", "potatoes", "burlap", "punch", "strike", "boxer", "gym", "grain", "flour"],
        "usage_notes": "Soldiers and laborers in the early 20th century referred to mattresses filled with hay or straw as sacks."
    }
}


def get_all_idioms():
    """Return list of all canonical idiom strings."""
    return list(IDIOM_DICTIONARY.keys())


def get_idiom_info(idiom_name):
    """Retrieve full metadata for a given canonical idiom or alias."""
    if not idiom_name:
        return None
    normalized = idiom_name.strip().lower()
    
    # Direct canonical match
    if normalized in IDIOM_DICTIONARY:
        return IDIOM_DICTIONARY[normalized]
    
    # Check aliases
    for key, info in IDIOM_DICTIONARY.items():
        if normalized == key:
            return info
        for alias in info.get("aliases", []):
            if normalized == alias.lower():
                return info
    return None
