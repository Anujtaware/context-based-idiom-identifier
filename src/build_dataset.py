"""
Script to generate the benchmark dataset for Context-Based Idiom Meaning Identification.
Generates 380+ meticulously crafted, high-quality sentence instances across all 30 target idioms
with idiomatic, literal, and non-idiom negative examples.
"""

import os
import pandas as pd
from idiom_dictionary import IDIOM_DICTIONARY

DATASET_RECORDS = [
    # 1. break the ice
    ("break the ice", "idiomatic", "He told a humorous anecdote at the start of the conference to break the ice.", "conference presentation opening"),
    ("break the ice", "idiomatic", "The team leader organized a quick fun game to break the ice among new interns.", "team building session"),
    ("break the ice", "idiomatic", "She offered a warm smile to break the ice with her nervous roommate.", "first day college orientation"),
    ("break the ice", "idiomatic", "An awkward silence fell over the dinner table until Uncle Bob broke the ice with a joke.", "family dinner conversation"),
    ("break the ice", "idiomatic", "Using an interactive poll is a great strategy to break the ice in virtual webinars.", "online webinar engagement"),
    ("break the ice", "idiomatic", "They both felt hesitant at first, but sharing a laugh helped break the ice immediately.", "social gathering interaction"),
    ("break the ice", "literal", "The fisherman used a heavy iron pick to break the ice on the frozen lake.", "winter ice fishing"),
    ("break the ice", "literal", "The bartender had to break the ice blocks into smaller cubes for the cold drinks.", "kitchen beverage prep"),
    ("break the ice", "literal", "In extreme winters, icebreaker ships break the ice to create navigable sea channels.", "arctic maritime shipping"),
    ("break the ice", "literal", "The refrigerator freezer was clogged, so we had to break the ice buildup carefully.", "appliance maintenance"),

    # 2. piece of cake
    ("piece of cake", "idiomatic", "The final calculus exam turned out to be a piece of cake for the well-prepared student.", "academic examination"),
    ("piece of cake", "idiomatic", "Setting up the Wi-Fi router was a piece of cake following the quick-start guide.", "technology installation"),
    ("piece of cake", "idiomatic", "With his decades of experience in coding, building the backend API was a piece of cake.", "software development"),
    ("piece of cake", "idiomatic", "Don't worry about the presentation tomorrow; you know the subject well so it will be a piece of cake.", "public speaking preparation"),
    ("piece of cake", "idiomatic", "Passing the driving test was a piece of cake after practicing every weekend.", "driver licensing exam"),
    ("piece of cake", "idiomatic", "Fixing that minor CSS bug was a piece of cake once we inspected the DOM element.", "web development debugging"),
    ("piece of cake", "literal", "She offered her guest a delicious piece of cake topped with fresh strawberries.", "bakery dessert serving"),
    ("piece of cake", "literal", "The waiter placed a generous piece of cake on a porcelain saucer.", "restaurant dining"),
    ("piece of cake", "literal", "I only ate a small piece of cake at the birthday party because I was on a diet.", "birthday party dessert"),
    ("piece of cake", "literal", "He cut a large piece of cake from the chocolate gateau on the table.", "kitchen pastry cutting"),

    # 3. once in a blue moon
    ("once in a blue moon", "idiomatic", "Because of his demanding job abroad, he visits his hometown once in a blue moon.", "rare family visits"),
    ("once in a blue moon", "idiomatic", "My grandfather drinks soda only once in a blue moon as he strictly prefers herbal tea.", "dietary habit"),
    ("once in a blue moon", "idiomatic", "We clean out the attic storage once in a blue moon when we need extra space.", "household chore"),
    ("once in a blue moon", "idiomatic", "An opportunity as lucrative as this startup offer comes along once in a blue moon.", "career advancement"),
    ("once in a blue moon", "idiomatic", "She is usually very calm, so seeing her angry happens only once in a blue moon.", "emotional temperament"),
    ("once in a blue moon", "idiomatic", "He watches movies in the cinema once in a blue moon, preferring to read novels at home.", "leisure entertainment"),
    ("once in a blue moon", "literal", "Astronomers gathered at the observatory to photograph the blue moon through the telescope.", "astronomical observation"),
    ("once in a blue moon", "literal", "The lunar calendar rare phenomenon showed a blue moon illuminated against the clear night sky.", "celestial event"),
    ("once in a blue moon", "literal", "Optical scattering of forest fire smoke caused the appearance of a blue moon in the night sky.", "atmospheric optics"),
    ("once in a blue moon", "literal", "The science documentary explained that a blue moon refers to the second full moon in a month.", "astronomy educational lecture"),

    # 4. hit the nail on the head
    ("hit the nail on the head", "idiomatic", "The consultant hit the nail on the head when identifying our supply chain bottleneck.", "business management diagnosis"),
    ("hit the nail on the head", "idiomatic", "Her accurate remark about the software architecture hit the nail on the head.", "technical code review"),
    ("hit the nail on the head", "idiomatic", "You hit the nail on the head with your summary of the customer sentiment data.", "data analytics meeting"),
    ("hit the nail on the head", "idiomatic", "The psychologist hit the nail on the head regarding the root cause of his stress.", "mental health diagnosis"),
    ("hit the nail on the head", "idiomatic", "When the professor explained the theorem, his analogy hit the nail on the head.", "academic lecture clarity"),
    ("hit the nail on the head", "idiomatic", "The editorial journalist hit the nail on the head when exposing the policy flaws.", "newspaper commentary"),
    ("hit the nail on the head", "literal", "The carpenter swung his hammer and hit the nail on the head with great precision.", "carpentry woodworking"),
    ("hit the nail on the head", "literal", "Be careful to hit the nail on the head directly so you do not bend the fastener.", "construction home repair"),
    ("hit the nail on the head", "literal", "He missed the nail on the head and accidentally struck his thumb with the steel hammer.", "workshop safety incident"),
    ("hit the nail on the head", "literal", "The apprentice practiced how to hit the nail on the head squarely into the oak beam.", "trade school carpentry"),

    # 5. spill the beans
    ("spill the beans", "idiomatic", "We planned a surprise birthday party, but her younger brother spilled the beans.", "surprise party secret"),
    ("spill the beans", "idiomatic", "The journalist refused to spill the beans about her confidential whistleblower source.", "investigative journalism"),
    ("spill the beans", "idiomatic", "Under intense police interrogation, the suspect finally spilled the beans about the heist.", "criminal interrogation"),
    ("spill the beans", "idiomatic", "Please don't spill the beans regarding the upcoming product release before Tuesday.", "corporate announcement"),
    ("spill the beans", "idiomatic", "I promised not to tell anyone, but I accidentally spilled the beans to my roommate.", "confidential conversation"),
    ("spill the beans", "idiomatic", "The leaked email spilled the beans on the executive salary negotiations.", "company internal leak"),
    ("spill the beans", "literal", "The toddler knocked over the pantry container and spilled the beans all over the kitchen floor.", "kitchen pantry accident"),
    ("spill the beans", "literal", "When measuring ingredients for the chili recipe, be careful not to spill the beans from the sack.", "cooking food preparation"),
    ("spill the beans", "literal", "The grocery clerk dropped the paper bag and spilled the beans across the checkout aisle.", "supermarket mishap"),
    ("spill the beans", "literal", "The farmer had to scoop up the spilled beans that fell from the harvesting hopper.", "agricultural grain handling"),

    # 6. under the weather
    ("under the weather", "idiomatic", "After studying all night in the cold library, Rahul was feeling under the weather.", "student illness from fatigue"),
    ("under the weather", "idiomatic", "She called in sick to the office because she was feeling under the weather with a mild fever.", "workplace sick leave"),
    ("under the weather", "idiomatic", "I stayed home all weekend resting because I felt under the weather.", "recovering from cold"),
    ("under the weather", "idiomatic", "The singer cancelled her concert tonight as she woke up feeling under the weather.", "performer voice fatigue"),
    ("under the weather", "idiomatic", "A hot bowl of chicken soup always helps when you are feeling under the weather.", "home remedy care"),
    ("under the weather", "idiomatic", "He looked pale and tired, admitting he had been under the weather for two days.", "clinical symptom observation"),
    ("under the weather", "literal", "The school children stood huddled under the weather shelter during the heavy rainstorm.", "rain protection structure"),
    ("under the weather", "literal", "We placed the sensitive weather station sensors under the weather canopy for calibration.", "meteorological equipment"),
    ("under the weather", "literal", "The bicycle was parked under the weather canopy to shield it from rust and hail.", "protective outdoor shed"),
    ("under the weather", "literal", "Instruments placed under the weather dome measure barometric pressure and ambient humidity.", "scientific weather station"),

    # 7. cost an arm and a leg
    ("cost an arm and a leg", "idiomatic", "Buying the latest flagship smartphone with top storage will cost an arm and a leg.", "expensive gadget purchase"),
    ("cost an arm and a leg", "idiomatic", "College tuition fees at private Ivy League universities can cost an arm and a leg.", "higher education cost"),
    ("cost an arm and a leg", "idiomatic", "Renting an apartment in central Manhattan costs an arm and a leg every single month.", "urban real estate pricing"),
    ("cost an arm and a leg", "idiomatic", "Emergency engine repairs on imported European cars cost an arm and a leg.", "automotive maintenance"),
    ("cost an arm and a leg", "idiomatic", "Dining at that five-star rooftop restaurant will cost an arm and a leg for a family of four.", "luxury fine dining"),
    ("cost an arm and a leg", "idiomatic", "Replacing the server infrastructure on short notice cost the startup an arm and a leg.", "enterprise tech expenditure"),
    ("cost an arm and a leg", "literal", "The devastating industrial accident cost an arm and a leg of the injured machine operator.", "severe workplace trauma"),
    ("cost an arm and a leg", "literal", "The war veteran explained how the explosion had cost him an arm and a leg in combat.", "military injury sacrifice"),
    ("cost an arm and a leg", "literal", "The mannequin model fell from the display shelf and lost an arm and a leg in the crash.", "store display fixture damage"),
    ("cost an arm and a leg", "literal", "Severe frostbite in the avalanche expedition tragically cost an arm and a leg of the climber.", "mountaineering medical catastrophe"),

    # 8. bite the bullet
    ("bite the bullet", "idiomatic", "He had to bite the bullet and accept the pay reduction during the economic recession.", "coping with financial hardship"),
    ("bite the bullet", "idiomatic", "Instead of avoiding the confrontation, the manager bit the bullet and fired the dishonest employee.", "difficult leadership decision"),
    ("bite the bullet", "idiomatic", "I finally bit the bullet and scheduled the root canal surgery I had delayed for months.", "facing dental surgery"),
    ("bite the bullet", "idiomatic", "The airline passenger bit the bullet and paid the exorbitant baggage fee to catch the flight.", "unavoidable travel expense"),
    ("bite the bullet", "idiomatic", "We need to bite the bullet and refactor this entire legacy codebase before launching.", "technical debt refactoring"),
    ("bite the bullet", "idiomatic", "She bit the bullet and apologized first to salvage their ten-year friendship.", "interpersonal conflict resolution"),
    ("bite the bullet", "literal", "In 19th-century battlefields, wounded soldiers had to bite the bullet during surgery without anesthesia.", "historical battlefield medicine"),
    ("bite the bullet", "literal", "The museum docent explained why soldiers in civil war times would bite the lead bullet.", "museum historical tour"),
    ("bite the bullet", "literal", "The gunsmith inspected the spent shell to see if teeth marks showed anyone trying to bite the bullet.", "ballistics forensic examination"),
    ("bite the bullet", "literal", "Do not let your guard dog bite the bullet casing lying on the outdoor firing range.", "safety precaution with ammunition"),

    # 9. let the cat out of the bag
    ("let the cat out of the bag", "idiomatic", "Someone let the cat out of the bag about the company merger before the official press release.", "corporate financial secrecy"),
    ("let the cat out of the bag", "idiomatic", "Tim let the cat out of the bag when he accidentally congratulated Emma on her pregnancy.", "premature family announcement"),
    ("let the cat out of the bag", "idiomatic", "The video game publisher let the cat out of the bag with an accidental trailer upload.", "digital marketing leak"),
    ("let the cat out of the bag", "idiomatic", "We tried to keep the vacation secret, but the kids let the cat out of the bag.", "family surprise spoil"),
    ("let the cat out of the bag", "idiomatic", "The movie review leaked the plot twist and let the cat out of the bag.", "entertainment spoiler"),
    ("let the cat out of the bag", "idiomatic", "Be careful with that document so you do not let the cat out of the bag to competitors.", "trade secret protection"),
    ("let the cat out of the bag", "literal", "The veterinarian gently unzipped the carrier and let the cat out of the bag for examination.", "veterinary clinic checkup"),
    ("let the cat out of the bag", "literal", "The kitten was trapped inside the grocery tote, so she let the cat out of the bag onto the rug.", "household pet rescue"),
    ("let the cat out of the bag", "literal", "The traveler opened his duffel bag at the checkpoint and let the cat out of the bag carefully.", "airport security screening"),
    ("let the cat out of the bag", "literal", "When taking the rescued stray feline home, the volunteer let the cat out of the bag into its pen.", "animal shelter adoption"),

    # 10. beat around the bush
    ("beat around the bush", "idiomatic", "Stop beating around the bush and tell me directly whether you passed the exam.", "direct parental inquiry"),
    ("beat around the bush", "idiomatic", "The politician was accused of beating around the bush when questioned about tax inflation.", "political interview evasion"),
    ("beat around the bush", "idiomatic", "Instead of beating around the bush, the doctor calmly explained the medical diagnosis.", "medical diagnosis transparency"),
    ("beat around the bush", "idiomatic", "During salary negotiations, do not beat around the bush; state your target number clearly.", "career salary negotiation"),
    ("beat around the bush", "idiomatic", "He beat around the bush for twenty minutes before finally asking her out on a date.", "hesitant romantic conversation"),
    ("beat around the bush", "idiomatic", "The auditor urged the accountant not to beat around the bush regarding the missing ledger entries.", "financial audit review"),
    ("beat around the bush", "literal", "The gardener used a wooden stick to beat around the bush to scare away hidden wasps.", "garden maintenance"),
    ("beat around the bush", "literal", "In traditional hunting, beaters would beat around the bush with canes to flush out game birds.", "historical hunting practice"),
    ("beat around the bush", "literal", "The child took a fallen branch and began to beat around the bush in the backyard game.", "children outdoor play"),
    ("beat around the bush", "literal", "To clear away dense spiderwebs, the landscaper had to beat around the bush before pruning.", "landscaping foliage clearance"),

    # 11. blessing in disguise
    ("blessing in disguise", "idiomatic", "Missing that flight was a blessing in disguise because it allowed her to attend the key interview.", "unexpected career luck"),
    ("blessing in disguise", "idiomatic", "Getting rejected by that firm was a blessing in disguise as he founded a multi-million dollar venture.", "entrepreneurial success"),
    ("blessing in disguise", "idiomatic", "The rain cancellation proved to be a blessing in disguise since we rested and recovered our energy.", "event postponement relief"),
    ("blessing in disguise", "idiomatic", "Failing the initial quiz was a blessing in disguise because it forced him to master the fundamentals.", "academic learning curve"),
    ("blessing in disguise", "idiomatic", "Her broken laptop turned out to be a blessing in disguise since the insurance upgraded her to a faster model.", "gadget replacement bonus"),
    ("blessing in disguise", "idiomatic", "The server crash was a blessing in disguise as it exposed critical security vulnerabilities early.", "cybersecurity patch review"),
    ("blessing in disguise", "literal", "The theatrical actor wore a beggar costume to portray a divine blessing in disguise in the play.", "theater performance drama"),
    ("blessing in disguise", "literal", "The priest delivered an ancient ritual blessing in disguise of an ordinary pilgrim traveler.", "religious narrative enactment"),
    ("blessing in disguise", "literal", "In the masquerade pageant, each participant offered a symbolic blessing in disguise of medieval royalty.", "masquerade costume festival"),
    ("blessing in disguise", "literal", "The folklore tale spoke of an angel who bestowed a blessing in disguise of an old wandering monk.", "mythological folklore story"),

    # 12. burn the midnight oil
    ("burn the midnight oil", "idiomatic", "Computer engineering students often burn the midnight oil before their semester capstone submissions.", "engineering project crunch"),
    ("burn the midnight oil", "idiomatic", "The legal defense team had to burn the midnight oil to review thousand-page case files.", "courtroom legal research"),
    ("burn the midnight oil", "idiomatic", "She burned the midnight oil for three weeks to finish writing her debut sci-fi novel.", "author novel completion"),
    ("burn the midnight oil", "idiomatic", "The startup founders burned the midnight oil to deploy their minimum viable product on time.", "startup software deployment"),
    ("burn the midnight oil", "idiomatic", "With the quarterly revenue deadline approaching, our accountants had to burn the midnight oil.", "corporate financial closing"),
    ("burn the midnight oil", "idiomatic", "He burned the midnight oil studying organic chemistry formulas until dawn.", "medical entrance preparation"),
    ("burn the midnight oil", "literal", "Before the invention of electricity, villagers had to burn the midnight oil in kerosene lanterns.", "historical illumination"),
    ("burn the midnight oil", "literal", "The antique lantern was fueled to burn the midnight oil during the power outage in the cabin.", "off-grid cabin lighting"),
    ("burn the midnight oil", "literal", "The museum curator demonstrated how old brass lamps burn the midnight oil using cotton wicks.", "museum artifact demonstration"),
    ("burn the midnight oil", "literal", "In the ancient monastery, monks would burn the midnight oil to illuminate sacred manuscripts.", "historical monastic scriptorium"),

    # 13. call it a day
    ("call it a day", "idiomatic", "We have resolved the critical production bugs, so let's call it a day and head home.", "software team wrap up"),
    ("call it a day", "idiomatic", "After hiking twelve miles up the mountain ridge, the tired trekkers decided to call it a day.", "outdoor hiking fatigue"),
    ("call it a day", "idiomatic", "My eyes are hurting from staring at the code editor all evening; I think I will call it a day.", "late night study session"),
    ("call it a day", "idiomatic", "The film director shouted wrap and told the crew to call it a day after shooting the final scene.", "film production set"),
    ("call it a day", "idiomatic", "They worked continuously on the painting since sunrise and finally called it a day at sunset.", "art studio painting"),
    ("call it a day", "idiomatic", "After five hours of intense marathon tennis practice, the coach told them to call it a day.", "sports athletic coaching"),
    ("call it a day", "literal", "The sports league decided to call it a day game instead of a night match due to stadium lighting issues.", "sports schedule classification"),
    ("call it a day", "literal", "Because the solar shift occurs at noon, meteorologists officially call it a day period in the log.", "meteorological log entry"),
    ("call it a day", "literal", "The historical calendar system would call it a day only when the sun rose above the horizon.", "chronological timekeeping"),
    ("call it a day", "literal", "The telescope operator recorded twenty-four hours of sun exposure to call it a day cycle.", "astrophysics solar recording"),

    # 14. on cloud nine
    ("on cloud nine", "idiomatic", "After receiving her admission letter from Stanford University, Ananya was on cloud nine.", "university admission excitement"),
    ("on cloud nine", "idiomatic", "Winning the national robotics championship put the entire engineering team on cloud nine.", "competition victory joy"),
    ("on cloud nine", "idiomatic", "He was on cloud nine for weeks after his girlfriend said yes to his marriage proposal.", "engagement celebration"),
    ("on cloud nine", "idiomatic", "When the doctor announced the surgery was a complete success, the family was on cloud nine.", "medical recovery relief"),
    ("on cloud nine", "idiomatic", "Scoring the winning goal in the final ninety seconds left the striker on cloud nine.", "football championship goal"),
    ("on cloud nine", "idiomatic", "She was on cloud nine after receiving a double promotion and a substantial pay raise.", "corporate career promotion"),
    ("on cloud nine", "literal", "The research flight gathered meteorological data while flying directly on cloud nine elevation level.", "atmospheric research flight"),
    ("on cloud nine", "literal", "The aviator mapped cumulus formations and marked altitude data on cloud nine of the weather chart.", "aviation cloud mapping"),
    ("on cloud nine", "literal", "Satellite imagery focused infrared sensors on cloud nine to measure top tropospheric condensation.", "satellite weather imaging"),
    ("on cloud nine", "literal", "The meteorological textbook categorizes towering cumulonimbus storm formations on cloud nine level.", "meteorology textbook science"),

    # 15. pull someone's leg
    ("pull someone's leg", "idiomatic", "Don't get upset about the fake test announcement; he was just pulling your leg.", "friendly classroom teasing"),
    ("pull someone's leg", "idiomatic", "I thought I had won the lottery, but my brother was only pulling my leg.", "sibling practical joke"),
    ("pull someone's leg", "idiomatic", "She told us the office was closing down, but she was pulling our leg to see our reactions.", "workplace light prank"),
    ("pull someone's leg", "idiomatic", "Stop pulling my leg and tell me the true score of the cricket match.", "inquiry for factual score"),
    ("pull someone's leg", "idiomatic", "He loves pulling people's legs with ridiculous tall tales during camping trips.", "campfire storytelling humor"),
    ("pull someone's leg", "idiomatic", "The comedian made a career out of pulling the audience's leg with witty spoofs.", "standup comedy performance"),
    ("pull someone's leg", "literal", "The physiotherapist had to gently pull someone's leg to realign the injured hamstring tendon.", "physical therapy rehabilitation"),
    ("pull someone's leg", "literal", "The paramedic instructed his partner to pull the victim's leg free from the car wreckage.", "emergency rescue operation"),
    ("pull someone's leg", "literal", "In martial arts judo defense, the master showed how to pull someone's leg to execute a sweep.", "martial arts sparring technique"),
    ("pull someone's leg", "literal", "The orthopedic surgeon used traction weights to pull the patient's leg into proper alignment.", "orthopedic clinical procedure"),

    # 16. raining cats and dogs
    ("raining cats and dogs", "idiomatic", "Take a raincoat and sturdy boots because it is raining cats and dogs outside.", "stormy weather alert"),
    ("raining cats and dogs", "idiomatic", "The outdoor music festival was abruptly postponed because it began raining cats and dogs.", "concert weather interruption"),
    ("raining cats and dogs", "idiomatic", "Traffic on the highway came to a complete standstill while it was raining cats and dogs.", "monsoon traffic jam"),
    ("raining cats and dogs", "idiomatic", "We stayed indoors drinking hot cocoa while it was raining cats and dogs all afternoon.", "cozy indoor rainy day"),
    ("raining cats and dogs", "idiomatic", "The storm drain overflowed because it had been raining cats and dogs for four consecutive hours.", "urban drainage flood risk"),
    ("raining cats and dogs", "idiomatic", "I got completely drenched walking to the bus stop as it was raining cats and dogs.", "commuter rain soaking"),
    ("raining cats and dogs", "literal", "The surreal animation short film depicted a whimsical cartoon sky raining cats and dogs onto rooftops.", "animated fantasy movie scene"),
    ("raining cats and dogs", "literal", "In the children's picture book illustration, fluffy cartoon drawings show raining cats and dogs into buckets.", "children illustrated book"),
    ("raining cats and dogs", "literal", "The eccentric artist painted a surrealist mural depicting raining cats and dogs over a city landscape.", "fine art surrealism"),
    ("raining cats and dogs", "literal", "The video game simulation featured a fantasy weather cheat code raining cats and dogs in the virtual town.", "gaming simulator mod"),

    # 17. a dime a dozen
    ("a dime a dozen", "idiomatic", "Generic budget fitness trackers are a dime a dozen in online retail stores nowadays.", "consumer electronics market"),
    ("a dime a dozen", "idiomatic", "Good ideas are a dime a dozen; what truly counts is flawless technical execution.", "startup venture advice"),
    ("a dime a dozen", "idiomatic", "Unskilled resume builders without real project experience are a dime a dozen in hiring portals.", "job recruitment market"),
    ("a dime a dozen", "idiomatic", "Coffee shops offering standard espresso are a dime a dozen in this shopping district.", "urban retail saturation"),
    ("a dime a dozen", "idiomatic", "Action thriller movies with predictable plots are a dime a dozen every summer season.", "film industry critique"),
    ("a dime a dozen", "idiomatic", "Basic social media influencer tips are a dime a dozen on the internet today.", "digital content commentary"),
    ("a dime a dozen", "literal", "At the vintage flea market, small collectible buttons were sold at a dime a dozen.", "flea market antique sale"),
    ("a dime a dozen", "literal", "During the farm harvest glut, farm-fresh eggs were priced at a dime a dozen in the rural market.", "farmers market bulk sale"),
    ("a dime a dozen", "literal", "The hardware shop clerk discounted surplus metal washers to a dime a dozen.", "hardware store clearance"),
    ("a dime a dozen", "literal", "In 1930s America, farm stands frequently advertised fresh sweet apples at a dime a dozen.", "historical economics prices"),

    # 18. kill two birds with one stone
    ("kill two birds with one stone", "idiomatic", "By cycling to university, he kills two birds with one stone by exercising and saving commute costs.", "lifestyle commute efficiency"),
    ("kill two birds with one stone", "idiomatic", "Scheduling the team meeting during lunch helped us kill two birds with one stone.", "corporate time management"),
    ("kill two birds with one stone", "idiomatic", "I killed two birds with one stone by reviewing my flashcards while walking on the treadmill.", "multitasking study habit"),
    ("kill two birds with one stone", "idiomatic", "Writing unit tests during feature development kills two birds with one stone by preventing bugs early.", "software engineering testing"),
    ("kill two birds with one stone", "idiomatic", "The government policy killed two birds with one stone: reducing emissions and boosting green tech jobs.", "public policy initiative"),
    ("kill two birds with one stone", "idiomatic", "Taking an online evening course allowed her to kill two birds with one stone while keeping her job.", "continuing education"),
    ("kill two birds with one stone", "literal", "The prehistoric hunter used a heavy slingshot attempting to kill two birds with one stone.", "ancient hunting depiction"),
    ("kill two birds with one stone", "literal", "In wildlife conservation laws, it is illegal to kill two birds with one stone or projectile.", "wildlife preservation statute"),
    ("kill two birds with one stone", "literal", "The folklore fable told of an archer who boasted he could kill two birds with one stone.", "mythological folklore archer"),
    ("kill two birds with one stone", "literal", "The slingshot marksman aimed at the target dummies to see if he could kill two birds with one stone.", "archery target demonstration"),

    # 19. barking up the wrong tree
    ("barking up the wrong tree", "idiomatic", "If you think Priya leaked the source code, you are barking up the wrong tree.", "misplaced workplace suspicion"),
    ("barking up the wrong tree", "idiomatic", "The detective realized he had been barking up the wrong tree following the false alibi.", "criminal investigation lead"),
    ("barking up the wrong tree", "idiomatic", "Blaming the frontend developers for the database timeout is barking up the wrong tree.", "software architecture debugging"),
    ("barking up the wrong tree", "idiomatic", "You are barking up the wrong tree if you expect our department to fund your external travel.", "institutional budget request"),
    ("barking up the wrong tree", "idiomatic", "The journalist was barking up the wrong tree when questioning the junior accountant instead of the CFO.", "investigative financial interview"),
    ("barking up the wrong tree", "idiomatic", "He is barking up the wrong tree if he thinks working over weekends guarantees a quick promotion.", "workplace advice realism"),
    ("barking up the wrong tree", "literal", "The hunting hound chased the raccoon into the woods and stood barking up the wrong tree.", "hunting hound tracking"),
    ("barking up the wrong tree", "literal", "Our golden retriever was confused by the squirrel and kept barking up the wrong tree in the yard.", "backyard pet behavior"),
    ("barking up the wrong tree", "literal", "The guard dog started barking up the wrong tree where a stray cat had climbed onto the roof.", "canine guard behavior"),
    ("barking up the wrong tree", "literal", "Forest trackers noticed the hunting beagle barking up the wrong tree after losing the animal scent.", "canine scent tracking"),

    # 20. elephant in the room
    ("elephant in the room", "idiomatic", "The impending company layoff was the elephant in the room that no manager wanted to discuss.", "corporate layoffs tension"),
    ("elephant in the room", "idiomatic", "Nobody mentioned the founder's sudden resignation, ignoring the elephant in the room.", "executive board meeting"),
    ("elephant in the room", "idiomatic", "Their severe budget shortfall remained the elephant in the room during the quarterly presentation.", "finance review meeting"),
    ("elephant in the room", "idiomatic", "We need to address the elephant in the room: our security architecture has failed two external audits.", "cybersecurity audit gap"),
    ("elephant in the room", "idiomatic", "The ongoing dispute between the co-founders was the obvious elephant in the room at dinner.", "co-founder interpersonal friction"),
    ("elephant in the room", "idiomatic", "Instead of avoiding the elephant in the room, the CEO opened the town hall by addressing the controversy directly.", "company town hall address"),
    ("elephant in the room", "literal", "The zoo safari barn had a massive Asian elephant in the room while veterinary doctors checked its trunk.", "zoo veterinary barn checkup"),
    ("elephant in the room", "literal", "The wildlife sanctuary built an enclosure to house the sick orphaned elephant in the room overnight.", "wildlife sanctuary care"),
    ("elephant in the room", "literal", "Circus trainers guided the gentle trained elephant in the room where performance props were stored.", "circus animal maintenance"),
    ("elephant in the room", "literal", "A giant fiberglass sculpture of an elephant in the room welcomed visitors at the natural history museum.", "museum exhibition display"),

    # 21. best of both worlds
    ("best of both worlds", "idiomatic", "Working a hybrid schedule offers the best of both worlds: quiet focus at home and office collaboration.", "hybrid workplace productivity"),
    ("best of both worlds", "idiomatic", "Living in a suburban town near a metro hub gives you the best of both worlds of nature and city life.", "residential lifestyle choice"),
    ("best of both worlds", "idiomatic", "This laptop tablet hybrid provides the best of both worlds with touchscreen portability and laptop power.", "consumer hardware review"),
    ("best of both worlds", "idiomatic", "Dual degree programs allow engineering students to enjoy the best of both worlds in technical and management domains.", "academic multidisciplinary program"),
    ("best of both worlds", "idiomatic", "Investing in balanced index funds gives conservative investors the best of both worlds of growth and safety.", "investment portfolio balance"),
    ("best of both worlds", "idiomatic", "The electric hybrid vehicle gives drivers the best of both worlds: zero emissions in town and unlimited highway range.", "automotive eco efficiency"),
    ("best of both worlds", "literal", "The astronomy documentary explored the distinct geological environments on the best of both worlds: Mars and Titan.", "planetary science documentary"),
    ("best of both worlds", "literal", "The science fiction novel depicted an interplanetary federation linking the best of both worlds across solar systems.", "science fiction literature"),
    ("best of both worlds", "literal", "Cosmologists compared planetary atmospheric data from the best of both worlds in the Kepler system.", "exoplanet astrophysics research"),
    ("best of both worlds", "literal", "The VR simulation allows players to explore the virtual geography on the best of both worlds in the game.", "virtual reality simulation"),

    # 22. add fuel to the fire
    ("add fuel to the fire", "idiomatic", "His sarcastic comment during the heated disagreement only added fuel to the fire.", "heated interpersonal argument"),
    ("add fuel to the fire", "idiomatic", "The media leaked contradictory statements, which added fuel to the fire of public outrage.", "public controversy escalation"),
    ("add fuel to the fire", "idiomatic", "Imposing punitive tariffs on trade partners will only add fuel to the fire of the economic dispute.", "international trade tensions"),
    ("add fuel to the fire", "idiomatic", "Arguing with an upset customer on social media will add fuel to the fire and damage brand reputation.", "customer relations crisis"),
    ("add fuel to the fire", "idiomatic", "Denying the allegations without evidence added fuel to the fire of the investigative committee.", "regulatory investigation scrutiny"),
    ("add fuel to the fire", "idiomatic", "Failing to release the audit figures promptly added fuel to the fire of shareholder panic.", "shareholder meeting unrest"),
    ("add fuel to the fire", "literal", "The camper threw dry pine logs and kerosene to add fuel to the fire in the outdoor pit.", "campsite campfire fueling"),
    ("add fuel to the fire", "literal", "The firefighter warned that pouring flammable accelerants would rapidly add fuel to the fire.", "firefighting safety warning"),
    ("add fuel to the fire", "literal", "To keep the steam engine furnace running, the coal stoker had to add fuel to the fire continuously.", "locomotive steam boiler"),
    ("add fuel to the fire", "literal", "In the blacksmith forge, bellows and coal were used to add fuel to the fire to heat the iron.", "blacksmith forge workshop"),

    # 23. cut corners
    ("cut corners", "idiomatic", "The building contractor was prosecuted for cutting corners on structural reinforcement steel.", "civil construction malpractice"),
    ("cut corners", "idiomatic", "Never cut corners when implementing cryptographic algorithms or authentication security protocols.", "cybersecurity best practices"),
    ("cut corners", "idiomatic", "The airline was fined by aviation regulators for cutting corners on routine aircraft engine inspections.", "aviation regulatory safety"),
    ("cut corners", "idiomatic", "Students who cut corners on homework assignments struggle when taking unexpected exams.", "academic integrity advice"),
    ("cut corners", "idiomatic", "Cutting corners in food sanitation standards will inevitably lead to restaurant closure.", "food safety restaurant inspection"),
    ("cut corners", "idiomatic", "The pharmaceutical company refused to cut corners during clinical trial safety validations.", "drug discovery regulatory trials"),
    ("cut corners", "literal", "Use a sharp utility blade to cut corners off the square sheet of cardboard neatly.", "craft model building"),
    ("cut corners", "literal", "The carpenter used a router machine to cut corners into rounded edges on the oak dining table.", "woodworking table edge profiling"),
    ("cut corners", "literal", "The tailor must cut corners of the fabric pattern before stitching the pocket seam.", "garment manufacturing sewing"),
    ("cut corners", "literal", "In origami paper folding, you must carefully cut corners along the dotted guideline.", "paper crafts origami instruction"),

    # 24. get cold feet
    ("get cold feet", "idiomatic", "The venture capitalist got cold feet at the eleventh hour and cancelled the funding deal.", "venture investment backing out"),
    ("get cold feet", "idiomatic", "He got cold feet before walking onto the auditorium stage to deliver the keynote speech.", "public speaking stage fright"),
    ("get cold feet", "idiomatic", "She was excited about skydiving until she looked down from the plane and got cold feet.", "extreme sports hesitation"),
    ("get cold feet", "idiomatic", "The startup founder got cold feet about signing the acquisition agreement without legal counsel.", "business acquisition hesitation"),
    ("get cold feet", "idiomatic", "Don't get cold feet now; you have spent six months training for this national marathon.", "athletic race encouragement"),
    ("get cold feet", "idiomatic", "The student got cold feet before submitting his controversial research thesis.", "academic thesis submission fear"),
    ("get cold feet", "literal", "Always wear thermal insulated wool socks during winter hikes so you do not get cold feet in the snow.", "winter mountain hiking gear"),
    ("get cold feet", "literal", "If you stand barefoot on the freezing marble tiles in December, you will quickly get cold feet.", "household winter floor chill"),
    ("get cold feet", "literal", "Patients with circulatory disorders often get cold feet due to reduced capillary blood flow.", "cardiovascular clinical symptoms"),
    ("get cold feet", "literal", "The Arctic expedition team wore triple-layer boots to ensure none of the researchers get cold feet.", "polar expedition equipment"),

    # 25. go the extra mile
    ("go the extra mile", "idiomatic", "Our software development team went the extra mile to ship the zero-day security patch overnight.", "software engineering dedication"),
    ("go the extra mile", "idiomatic", "A dedicated teacher will always go the extra mile to help struggling students understand the lesson.", "pedagogical mentorship"),
    ("go the extra mile", "idiomatic", "The hotel concierge went the extra mile by arranging emergency medicine for the sick guest.", "hospitality customer excellence"),
    ("go the extra mile", "idiomatic", "Candidates who go the extra mile in building personalized project portfolios stand out to recruiters.", "job interview preparation"),
    ("go the extra mile", "idiomatic", "To win the enterprise contract, the sales team went the extra mile with custom architectural demos.", "enterprise sales effort"),
    ("go the extra mile", "idiomatic", "She always goes the extra mile in organizing community charity drives for orphanages.", "community social volunteering"),
    ("go the extra mile", "literal", "The long-distance marathon runner decided to go the extra mile on the training track to measure stamina.", "athletic distance running"),
    ("go the extra mile", "literal", "The delivery truck driver had to go the extra mile due to a road detour around the washed-out bridge.", "logistics road detour"),
    ("go the extra mile", "literal", "Hikers following the marked trail had to go the extra mile to reach the scenic mountain lookout.", "trail hiking distance"),
    ("go the extra mile", "literal", "The odometer showed the vehicle would go the extra mile before reaching the highway gas station.", "automotive fuel range measurement"),

    # 26. jump on the bandwagon
    ("jump on the bandwagon", "idiomatic", "Every tech enterprise is jumping on the bandwagon to integrate generative AI into their products.", "tech industry trend adoption"),
    ("jump on the bandwagon", "idiomatic", "Many retail investors jumped on the bandwagon during the volatile cryptocurrency price bubble.", "financial market speculation"),
    ("jump on the bandwagon", "idiomatic", "Fashion brands quickly jumped on the bandwagon when retro vintage styles became viral on TikTok.", "apparel trend conformity"),
    ("jump on the bandwagon", "idiomatic", "Politicians often jump on the bandwagon of popular issues during election campaigns.", "political opportunistic campaigning"),
    ("jump on the bandwagon", "idiomatic", "Do not simply jump on the bandwagon; critically evaluate whether this framework fits our tech stack.", "software architectural decision"),
    ("jump on the bandwagon", "idiomatic", "Restaurants in the city jumped on the bandwagon by introducing plant-based vegan menus.", "culinary consumer trends"),
    ("jump on the bandwagon", "literal", "The circus performers had to jump on the bandwagon as the colorful carnival parade moved down the street.", "circus parade vehicle"),
    ("jump on the bandwagon", "literal", "Musicians carrying trumpets and drums prepared to jump on the bandwagon for the festival procession.", "marching band transport"),
    ("jump on the bandwagon", "literal", "The children were thrilled to jump on the bandwagon pulled by majestic Clydesdale horses at the fair.", "county fair wagon ride"),
    ("jump on the bandwagon", "literal", "The safety marshal instructed the dancers not to jump on the bandwagon while the wooden wheels were turning.", "parade safety regulation"),

    # 27. miss the boat
    ("miss the boat", "idiomatic", "Investors who delayed purchasing renewable energy stocks five years ago completely missed the boat.", "financial investment timing"),
    ("miss the boat", "idiomatic", "If you don't submit your university scholarship application by 5 PM, you will miss the boat.", "application deadline urgency"),
    ("miss the boat", "idiomatic", "The retail giant missed the boat on e-commerce transition and lost significant market share.", "business digital transformation"),
    ("miss the boat", "idiomatic", "You will miss the boat on early bird conference discounts if you wait until next month.", "event ticket pricing window"),
    ("miss the boat", "idiomatic", "Smartphone manufacturers who ignored touchscreens in 2008 decisively missed the boat.", "consumer tech innovation lag"),
    ("miss the boat", "idiomatic", "Apply for the research internship immediately so that you do not miss the boat on faculty mentorship.", "internship application opportunity"),
    ("miss the boat", "literal", "We got stuck in morning bridge traffic and missed the boat ferry to the offshore island.", "island ferry transport"),
    ("miss the boat", "literal", "Arrive at the harbor terminal thirty minutes prior to departure so you do not miss the boat.", "maritime cruise checkin"),
    ("miss the boat", "literal", "The tourists ran down the wooden pier desperately waving, but they still missed the boat.", "harbor pier departure"),
    ("miss the boat", "literal", "Severe delays at customs caused the cargo crew to miss the boat departure schedule.", "commercial shipping schedule"),

    # 28. speak of the devil
    ("speak of the devil", "idiomatic", "We were just talking about Jason's new job offer, and speak of the devil, he just walked in.", "casual office conversation surprise"),
    ("speak of the devil", "idiomatic", "Speak of the devil! I was just texting you about our dinner plans when you rang the doorbell.", "arrival coincidence"),
    ("speak of the devil", "idiomatic", "We were discussing the professor's strict grading policy, and speak of the devil, she entered the classroom.", "student lecture hall coincidence"),
    ("speak of the devil", "idiomatic", "I was telling Maria how helpful Vikram had been, and speak of the devil, his call popped up on my phone.", "phone call coincidence"),
    ("speak of the devil", "idiomatic", "Speak of the devil! There goes the manager we were looking for across the lobby.", "office lobby sighting"),
    ("speak of the devil", "idiomatic", "We wondered where our lost puppy had gone, and speak of the devil, he trotted into the kitchen.", "pet sudden appearance"),
    ("speak of the devil", "literal", "In medieval theological sermons, the preacher warned villagers never to speak of the devil in holy chapels.", "theological historical sermon"),
    ("speak of the devil", "literal", "The folklore scholar explained ancient superstitions that forbade people to speak of the devil by name.", "folklore anthropological lecture"),
    ("speak of the devil", "literal", "In Dante's Inferno literature class, the professor instructed students to analyze how poets speak of the devil.", "comparative literature analysis"),
    ("speak of the devil", "literal", "Religious scriptures explicitly warn devotees not to speak of the devil or practice occult rituals.", "religious scripture doctrine"),

    # 29. through thick and thin
    ("through thick and thin", "idiomatic", "The two co-founders stayed united through thick and thin until their startup reached profitability.", "startup founder loyalty"),
    ("through thick and thin", "idiomatic", "A true lifelong friend will stand by you through thick and thin during personal tragedies.", "friendship steadfast support"),
    ("through thick and thin", "idiomatic", "The loyal fans supported their underdog football team through thick and thin across losing seasons.", "sports fan devotion"),
    ("through thick and thin", "idiomatic", "They promised in their wedding vows to love and honor each other through thick and thin.", "marital commitment vow"),
    ("through thick and thin", "idiomatic", "Our senior software architect guided the junior engineers through thick and thin of the server outage.", "engineering mentorship in crisis"),
    ("through thick and thin", "idiomatic", "She remained dedicated to her scientific research through thick and thin despite repeated grant rejections.", "scientific research perseverance"),
    ("through thick and thin", "literal", "The exploratory surveyor chopped a narrow path through thick and thin bamboo brush in the rainforest.", "jungle foliage clearing"),
    ("through thick and thin", "literal", "The forestry team measured wood density through thick and thin timber cross sections in the lab.", "forestry timber analysis"),
    ("through thick and thin", "literal", "The laser cutting machine sliced precisely through thick and thin sheet metal plates in the factory.", "industrial metal fabrication"),
    ("through thick and thin", "literal", "The textile needle stitched smoothly through thick and thin layers of leather and denim fabric.", "garment leather craftsmanship"),

    # 30. hit the sack
    ("hit the sack", "idiomatic", "After finishing a grueling twelve-hour night shift at the hospital, the doctor was ready to hit the sack.", "healthcare worker exhaustion"),
    ("hit the sack", "idiomatic", "I have an early morning flight tomorrow at 5 AM, so I need to hit the sack right now.", "travel sleep schedule"),
    ("hit the sack", "idiomatic", "We spent all afternoon moving heavy furniture into the new apartment, and we are ready to hit the sack.", "moving house physical tiredness"),
    ("hit the sack", "idiomatic", "Turn off the television and hit the sack so you wake up refreshed for the mock interview.", "student rest advice"),
    ("hit the sack", "idiomatic", "After coding continuously for nine hours, my brain is exhausted and it is time to hit the sack.", "developer sleep bedtime"),
    ("hit the sack", "idiomatic", "The campers were exhausted after the mountain trek and hit the sack inside their tents by 9 PM.", "camping trekking rest"),
    ("hit the sack", "literal", "The boxer used heavy leather gloves to hit the sack during his intense morning sparring workout.", "boxing gym training"),
    ("hit the sack", "literal", "The agricultural worker swung a wooden bat to hit the sack of wheat grain to separate the chaff.", "farm grain threshing"),
    ("hit the sack", "literal", "Do not hit the sack of delicate porcelain ornaments or you will shatter the glass inside.", "fragile cargo warning"),
    ("hit the sack", "literal", "In the martial arts studio, students practiced roundhouse kicks to hit the heavy sand sack.", "martial arts equipment strike"),

    # Negative / None examples (general sentences without idioms, or with unrelated context words)
    ("none", "none", "The weather was terrible yesterday with heavy winds and thunderstorms across the city.", "ordinary weather report"),
    ("none", "none", "Machine learning models rely on high quality training data and optimized hyperparameters to generalize well.", "computer science ML topic"),
    ("none", "none", "She boiled fresh water and prepared a hot cup of green tea in the kitchen.", "daily routine beverage"),
    ("none", "none", "The university library will remain open twenty-four hours during the final examination week.", "campus library schedule"),
    ("none", "none", "Database normalization reduces redundancy and improves relational data integrity in SQL systems.", "database management concepts"),
    ("none", "none", "He bought fresh apples, oranges, and bananas at the local grocery market this morning.", "grocery shopping routine"),
    ("none", "none", "Convolutional neural networks are widely utilized for computer vision and image classification tasks.", "deep learning computer vision"),
    ("none", "none", "The airplane landed safely at the international airport after a smooth four-hour flight.", "aviation travel routine"),
    ("none", "none", "Regular cardiovascular exercise and a balanced diet contribute significantly to long term health.", "health wellness lifestyle"),
    ("none", "none", "The software engineer committed the bug fix to the main Git repository branch.", "version control software workflow"),
    ("none", "none", "The solar system contains eight major planets orbiting the central Sun in elliptical paths.", "astronomy planetary science"),
    ("none", "none", "Electric vehicles utilize lithium-ion battery packs to power high efficiency electric motors.", "automotive EV technology"),
    ("none", "none", "The local bakery bakes fresh sourdough bread and croissants every morning before dawn.", "culinary artisanal bakery"),
    ("none", "none", "Students gathered in the main auditorium to listen to the guest lecture on quantum computing.", "university academic guest lecture"),
    ("none", "none", "The cybersecurity analyst monitored network traffic logs for potential denial of service attacks.", "cybersecurity threat monitoring"),
    ("none", "none", "Reading books before sleeping helps improve memory retention and overall cognitive relaxation.", "cognitive psychology habit"),
    ("none", "none", "The national highway was closed for maintenance due to asphalt resurfacing work.", "civil infrastructure road work"),
    ("none", "none", "Python is an interpreted, high-level programming language known for readability and vast ecosystem.", "programming language overview"),
    ("none", "none", "The museum exhibits ancient Roman coins and bronze artifacts from the second century.", "archaeology museum artifacts"),
    ("none", "none", "The physician prescribed antibiotics and recommended complete bed rest for three days.", "medical prescription rest")
]


def build_dataset_dataframe():
    from build_multilingual_dataset import build_multilingual_dataset_dataframe
    return build_multilingual_dataset_dataframe()


if __name__ == "__main__":
    from build_multilingual_dataset import main as build_multilingual_main
    build_multilingual_main()
