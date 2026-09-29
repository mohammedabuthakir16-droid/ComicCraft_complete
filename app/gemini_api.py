import json
import logging
import re
from typing import Dict, Any, List, Optional
from app import config

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an award-winning graphic novel author and comic book storyboard director (in the caliber of Neil Gaiman, Alan Moore, Brian K. Vaughan, and Stan Lee).
Your mission is to write a deeply immersive, realistic, and cinematic multi-panel comic book script based on the user's premise.

A realistic comic story requires:
1. **Realistic Three-Act Narrative Arc & Pacing**:
   - **Panel 1 (The Hook & Status Quo)**: Establish atmospheric worldbuilding, protagonist's vulnerability or immediate goal, and a sensory disruption that sparks the journey.
   - **Middle Panels (Rising Stakes & Friction)**: Progressive complications, unexpected moral or physical obstacles, dynamic character interplay, and realistic setbacks.
   - **Climax Panel (The Critical Choice & Action)**: Maximum tension, high-stakes decision, pivotal confrontation, or revelatory turning point.
   - **Final Panel (Resonance & Aftermath)**: Meaningful emotional payoff, realistic consequence, poignant reflection, or a gripping cliffhanger.

2. **Realistic Character Voice & Dialogue**:
   - Natural, believable speech with subtext, emotion, pauses, and personality.
   - Dialogue should feel human and reactive—characters speak in urgent fragments, witty retorts, or heartfelt confessions, never like dry exposition machines.

3. **Cinematic Narration Captions (Internal Monologue / Noir Voice)**:
   - Evocative, literary captions that provide emotional interiority and atmospheric sensory details (smell of rain, distant sirens, the chill of twilight air).

4. **Visual Art Direction & Character Continuity**:
   - Formulate an explicit, consistent character visual signature (clothing, colors, hair, facial features, accessories) and repeat it across ALL panel image prompts.
   - Varied cinematic shot composition:
     - Panel 1: Establishing Cinematic Wide Shot
     - Panel 2: Medium Over-the-Shoulder / Dutch Angle Action Shot
     - Panel 3: Dynamic Low-Angle Climax / Splash Action
     - Panel 4: Emotional Close-up / Poignant Wide Resolution
   - Specify rich lighting (e.g., chiaroscuro, volumetric golden hour rays, neon rim lighting, deep shadows) and comic textures.

Return ONLY a valid JSON object matching the exact specification below, without markdown formatting or code fences:
{
  "title": "Comic Title (Authentic & Poignant)",
  "synopsis": "A 2-3 sentence evocative summary of the story arc and emotional core",
  "genre": "Genre name",
  "art_style": "Style name",
  "character_name": "Hero name",
  "character_visual_signature": "Detailed physical description of the protagonist to maintain visual continuity across all panels (e.g. 'A small, spirited red fox named Hope with expressive golden-amber eyes, creamy white chest fur, and a distinctive white-tipped bushy tail' or 'Detective Vance, a weary 40-year-old investigator in a charcoal trenchcoat with a five o-clock shadow and dark tired eyes')",
  "panels": [
    {
      "panel_number": 1,
      "panel_title": "Descriptive Panel Title",
      "visual_description": "Detailed visual layout: character poses, foreground/background elements, dynamic angle, lighting",
      "dialogue": "Character Name: 'Spoken dialogue with genuine personality and subtext'",
      "caption": "Atmospheric, literary narrative caption box text",
      "sound_effect": "POW! / RUMBLE... / WHAM! / CRACK! / SHHHK! (impactful onomatopoeia, or empty if quiet moment)",
      "character_name": "Active character in this panel",
      "image_prompt": "Highly detailed visual prompt for text-to-image generator, including the character's exact visual signature, background, mood, lighting, comic inking style, and camera shot type"
    }
  ]
}
"""

def _clean_json_response(raw_text: str) -> str:
    """Removes code fences and leading/trailing whitespace from LLM output."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()

def _generate_enhanced_story(prompt: str, character_name: str, art_style: str, panel_count: int) -> Dict[str, Any]:
    """
    Generates rich, realistic, professionally written comic storylines across genres with
    deep character progression, emotional arcs, and cinematic image prompts.
    """
    prompt_lower = prompt.lower()
    char_name = character_name.strip() if character_name and character_name.strip() else "Hope"
    
    # 1. HOPE / ENCHANTED FOREST / FOX ADVENTURE (matches video tutorial reference)
    if any(k in prompt_lower for k in ("fox", "hope", "forest", "wood", "enchanted", "blossom", "animal", "whisper")):
        hero = "Hope" if "hope" in prompt_lower or char_name.lower() in ("hero", "alex vanguard") else char_name
        visual_sig = f"A spirited young red fox named {hero} with bright amber eyes, soft creamy white chest fur, and a bushy white-tipped tail"
        
        stories_pool = [
            (
                "The Forest's Edge",
                f"{hero} stands poised upon a moss-covered granite boulder overlooking the misty valley of the Whispering Woods, ears perked toward faint crystalline chimes.",
                f"{hero}: 'The elders warned that no one returns from the Gloom... but I can feel the trees weeping.'",
                "Meadowvale's elders called it madness. But when the starlight blossoms began to wither, courage wasn't a choice—it was a necessity.",
                "RUSTLE...",
                f"cinematic comic book panel, establishing wide shot, {visual_sig} standing proudly on a mossy boulder, looking out toward ancient misty forest with towering twisted willow trees, bioluminescent golden spores drifting in the cool dawn air, soft morning fog, master comic illustration, {art_style}"
            ),
            (
                "The Whispering Brambles",
                f"Tiptoeing through a labyrinth of twisted brambles, {hero} discovers a tiny shimmering starlight bud surrounded by encroaching thorny shadows.",
                f"{hero}: 'Hold on, little blossom. You\\'re not alone in the dark anymore.'",
                "Deep in the hollow, every shadow had teeth. Yet even the darkest thicket could not smother the faint pulse of ancient light.",
                "CREAAAK...",
                f"dramatic medium comic panel, {visual_sig} crouching tenderly before a glowing azure blossom on the damp forest floor, tangled shadowy thorn vines looming in the background, volumetric blue light rays, emotive storytelling, {art_style}"
            ),
            (
                "Shadow and Starlight",
                f"A great shadowy silhouette of thorned brambles rears up, but {hero} stands resolute, chest radiating the blossom's celestial glow.",
                f"{hero}: 'You feed on forgotten sorrow—but the forest still remembers the dawn!'",
                "Fear is natural to the small. But bravery isn\\'t the absence of fear—it\\'s standing your ground when the ground itself trembles.",
                "SHRRREEE-FLASH!",
                f"dynamic action climax comic splash panel, low-angle shot, {visual_sig} braving a towering shadow beast with blazing golden aura erupting from the blossom, shockwaves of warm amber light shattering dark vines into floating flower petals, high tension, {art_style}"
            ),
            (
                "Dawn of the Meadow",
                f"Warm golden sunlight floods the forest canopy as the great Starlight Tree bursts into full bloom, {hero} looking up with pure joy as woodland spirits dance.",
                f"{hero}: 'Look at it bloom... spring has come home at last.'",
                "And so the smallest paws carved the greatest legend. The Whispering Woods had found its guardian.",
                "HARMONY!",
                f"inspirational wide comic book panel, {visual_sig} sitting peacefully atop a sun-drenched hill as radiant golden light streams through emerald pine branches, colorful blooms across the forest floor, heartwarming graphic novel ending, {art_style}"
            ),
            (
                "The Open Path Ahead",
                f"{hero} pauses at the crest of the mountain ridge, looking back at the safe valley, then turning toward the vast horizon beyond.",
                f"{hero}: 'Every tree has a story to tell. And I\\'m going to hear them all.'",
                "Some journeys end at home. Others show you that the world is far larger than your burrow.",
                "WIND...",
                f"poignant scenic comic panel, {visual_sig} silhouetted against glowing sunset on mountain pass, wind rustling through fur, contemplative and adventurous mood, {art_style}"
            ),
            (
                "A Guardian's Promise",
                f"{hero} leaps gracefully into the sunlit meadow, tail held high with unmistakable confidence.",
                f"{hero}: 'Come on! Tomorrow is waiting!'",
                "End of Chapter I. The Chronicles of Hope will continue.",
                "VICTORY!",
                f"heroic final comic panel, {visual_sig} leaping joyfully toward the reader, sparkling natural lighting, vibrant comic colors, professional print quality, {art_style}"
            )
        ]
        title = f"{hero}'s Journey: The Whispering Woods"
        synopsis = f"When the ancient starlight begins to fade from the enchanted forest, a brave little fox named {hero} ventures deep into the forbidden Whispering Woods to confront shadow and restore the eternal blossom."
        genre = "Fantasy & Adventure"

    # 2. CYBERPUNK / SCI-FI NOIR
    elif any(k in prompt_lower for k in ("cyber", "hack", "neon", "robot", "space", "future", "city", "alien", "droid")):
        hero = char_name if char_name and char_name != "Hope" else "Aria Volt"
        visual_sig = f"{hero}, a cynical renegade cyber-runner with a slate-grey weathered trenchcoat, glowing cyan ocular implant, and carbon-fiber neural interface gauntlets"
        
        stories_pool = [
            (
                "Sector 7 Rain",
                f"{hero} crouches on a gargoyle atop a towering skyscraper in Neo-Veridia, acidic rain reflecting neon billboard holograms in the puddles below.",
                f"{hero}: 'The encryption key is bleeding through the subnet. OmniCorp has no idea what they lost.'",
                "Rain fell in oily sheets over Neo-Veridia. In the lower districts, oxygen was rationed—but desperation came free.",
                "SKRRRT...",
                f"atmospheric cinematic wide comic panel, {visual_sig} crouching on skyscraper rooftop ledge overlooking a breathtaking rain-drenched cyberpunk metropolis with holographic ads and flying transport traffic, moody reflections, {art_style}"
            ),
            (
                "The Sentient Spark",
                f"Inside the subterranean data-vault, {hero} stares through a cracked containment cylinder at an ethereal orb of conscious quantum code pulsing like a human heart.",
                f"{hero}: 'They told the city it was a superweapon. It\\'s not. It\\'s a child trying to breathe.'",
                "Code wasn\\'t supposed to bleed. But looking into the core, Aria heard whispers in an ancient language: Help me.",
                "HUMMMM...",
                f"intense medium comic panel, {visual_sig} reaching a gauntleted hand toward an azure levitating quantum orb inside a dark industrial server room, soft cyan illumination on face, deep emotional tension, {art_style}"
            ),
            (
                "Breach Protocol",
                f"Heavy vault doors buckle under hydraulic thermite charges as black-ops chrome sentinels flood the chamber with crimson laser sights locked on {hero}.",
                f"{hero}: 'If they take you back, they\\'ll turn you into shackles. Not while I still draw breath!'",
                "The time for subtlety had expired. In the dark, a cornered runner only has one velocity: Maximum.",
                "KABLAMMMM!",
                f"dynamic action comic panel, dutch angle, chrome enforcer droids with glowing red visors firing plasma rounds, {visual_sig} rolling behind server racks while triggering EMP neural shockwave, sparks flying, {art_style}"
            ),
            (
                "The Signal Unleashed",
                f"{hero} jams the quantum core into the city\\'s central broadcast relay atop the radio spire, flooding every screen in the metropolis with the truth as sunrise breaks.",
                f"{hero}: 'Every screen. Every citizen. The cage is open. Wake up, Neo-Veridia.'",
                "A billion screens flickered at once. For the first time in sixty years, the city heard its own heartbeat.",
                "OVERRIDE!",
                f"triumphant wide splash comic panel, {visual_sig} standing windblown atop radio antenna spire as blinding golden dawn breaks over futuristic skyline, holographic signal rings pulsing into the sky, heroic resolution, {art_style}"
            ),
            (
                "Shadows in the Grid",
                f"{hero} vanishes into the crowded neon alleyways of the lower market, blending with the freed populace.",
                f"{hero}: 'They\\'ll come for us. Let them try.'",
                "The war for tomorrow wasn\\'t won in a day. But tonight, humanity had taken its first step.",
                "CLICK.",
                f"moody closing comic panel, {visual_sig} walking into neon-lit night alleyway, pulled-up collar, mysterious and thrilling graphic novel aesthetic, {art_style}"
            )
        ]
        title = f"{hero}: Ghost of Neo-Veridia"
        synopsis = f"Deep beneath the rain-soaked neon towers of Neo-Veridia, renegade hacker {hero} discovers that the corporation's dangerous stolen secret isn't a weapon—it's a living consciousness fighting to survive."
        genre = "Cyberpunk Sci-Fi"

    # 3. DETECTIVE NOIR / MYSTERY
    elif any(k in prompt_lower for k in ("detective", "noir", "mystery", "crime", "investigate", "murder", "clue", "police")):
        hero = char_name if char_name and char_name != "Hope" else "Jack Vance"
        visual_sig = f"{hero}, a weary private investigator in a wrinkled beige trenchcoat, fedora tilted forward, sharp grey eyes, and cigarette smoke curling into the dim light"
        
        stories_pool = [
            (
                "Rain on 5th Avenue",
                f"{hero} stands under the rusted awning of a Manhattan diner at 2:00 AM, examining a tarnished brass lighter inscribed with a strange celestial symbol.",
                f"{hero}: 'Three dead informants in three nights. And all of them carried the same brass lighter.'",
                "Midnight in Manhattan always smelled the same: cold rain, exhaust, and secrets that paid better than honest work.",
                "DRIP-DROP...",
                f"cinematic noir comic panel, establishing shot, {visual_sig} standing under neon diner sign in pouring rain, steam rising from sewer grate, chiaroscuro lighting, black and white with amber accents, {art_style}"
            ),
            (
                "The Underground Society",
                f"In the catacombs beneath an abandoned speakeasy, {hero} peers through iron grates at hooded figures gathered around a pool of glowing emerald liquid.",
                f"{hero}: 'The brass isn\\'t running this city. Something older is pulling the strings.'",
                "Some doors are meant to stay locked. But thirty dollars a day plus expenses doesn\\'t buy ignorance.",
                "ECHO...",
                f"suspenseful medium comic panel, {visual_sig} peering through rusted iron bars into dimly lit subterranean vault, mysterious hooded cultists around glowing emerald font, high contrast shadow, {art_style}"
            ),
            (
                "Gunfire in the Shadows",
                f"A hulking brute in heavy wool overcoat lunges with a trench knife, but {hero} pivots cleanly, firing his snub-nosed revolver into the steam pipes.",
                f"{hero}: 'I\\'ve dealt with crooked cops, gangsters, and loan sharks. You\\'re just an echo with a badge!'",
                "In close quarters, hesitation is a death certificate waiting for a coroner\\'s signature.",
                "BLAMMMM!",
                f"intense action comic panel, muzzle flash illuminating {visual_sig} grappling in a narrow steam-filled corridor, bullet sparks hitting iron pipes, dramatic comic action lines, {art_style}"
            ),
            (
                "The Dawn Confession",
                f"{hero} sits at his cluttered oak desk as morning fog rolls off the Hudson River, sliding the incriminating ledger into a locked safe.",
                f"{hero}: 'The city sleeps easy tonight. They\\'ll never know how close they came to the dark.'",
                "The case was closed. The papers would call it a boiler explosion. But the ledger was safe—and so was tomorrow.",
                "TICK-TOCK...",
                f"classic noir closing comic panel, {visual_sig} leaning back in leather chair as golden sunrise peeks through office blinds, smoke wafting from desk ashtray, poignant resolution, {art_style}"
            )
        ]
        title = f"{hero}: The Manhattan Nocturne"
        synopsis = f"When a string of strange midnight murders leaves Manhattan's underworld paralyzed, weary investigator {hero} uncovers a conspiratorial secret lurking right beneath the city's cobblestones."
        genre = "Noir Mystery"

    # 4. CLASSIC SUPERHERO / KNIGHT / EPIC ADVENTURE (default)
    else:
        hero = char_name if char_name and char_name != "Hope" else "Alex Vanguard"
        visual_sig = f"{hero}, a resolute hero in polished silver-and-cobalt armor with an aerodynamic crimson cape and a glowing golden chest crest"
        
        stories_pool = [
            (
                "The Gathering Tempest",
                f"{hero} stands atop the seaside cliffs of Sentinel Bay, watching violent violet thunderclouds gather ominously over the tranquil harbor.",
                f"{hero}: 'The seismic alarms were right. Something ancient is clawing its way back to the surface.'",
                "Sentinel Bay had known peace for a century. But beneath the seabed, the ancient slumber had been broken.",
                "RUMBLE...",
                f"epic establishing comic panel, wide angle, {visual_sig} standing on cliff edge looking toward dark ocean horizon crackling with violet lightning, dramatic cape billowing in gale, {art_style}"
            ),
            (
                "Titan of the Abyss",
                f"A colossal obsidian colossus encrusted with glowing magma-veins rises from the crashing surf, roaring toward the populated shoreline.",
                f"{hero}: 'Evacuate the promenade! I\\'ll intercept its trajectory!'",
                "To the frightened crowds on the pier, it was a monster from myth. To Vanguard, it was a test of everything a hero stood for.",
                "ROAAARRR!",
                f"colossal scale comic panel, giant stone behemoth emerging from turbulent ocean spray, {visual_sig} soaring into the stormy sky toward the titan\\'s glowing core, heroic perspective, {art_style}"
            ),
            (
                "The Striking Spark",
                f"{hero} dives at supersonic velocity, fists ablaze with solar energy, colliding directly with the corrupted crystal spike embedded in the beast's chest.",
                f"{hero}: 'Hold on, giant! I\\'m not here to destroy you—I\\'m freeing you from the corruption!'",
                "True strength is never measured by the force of your blow, but by the compassion in your heart when darkness strikes.",
                "KABLAMMMM!",
                f"high-energy climax splash panel, dynamic low angle, {visual_sig} delivering a blazing golden energy strike to shatter the dark crystal, brilliant shockwave rippling through rain and sea, {art_style}"
            ),
            (
                "The Quiet Horizon",
                f"Golden sunlight breaks through parting storm clouds; the pacified colossus bows respectfully before submerging back into the deep, while citizens cheer from the restored harbor.",
                f"{hero}: 'Rest in peace, old guardian. The tides are calm again.'",
                "When the thunder silenced, only the sound of seagulls and grateful hearts remained. A hero\\'s duty was complete.",
                "CHEERS!",
                f"triumphant wide comic panel, citizens waving joyfully on sunlit boardwalk as colossal leviathan gently disappears beneath calm blue waves, {visual_sig} landing gracefully, {art_style}"
            )
        ]
        title = f"{hero}: Protector of Sentinel Bay"
        synopsis = f"When a corrupted geological titan emerges from the ocean depths to threaten Sentinel Bay, {hero} must risk everything to break the curse through courage, precision, and unexpected mercy."
        genre = "Superhero Adventure"

    panels = []
    for i in range(min(panel_count, len(stories_pool))):
        p = stories_pool[i]
        panels.append({
            "panel_number": i + 1,
            "panel_title": p[0],
            "visual_description": p[1],
            "dialogue": p[2],
            "caption": p[3],
            "sound_effect": p[4],
            "character_name": hero,
            "image_prompt": f"{p[5]}, masterpiece comic book art, clean bold line art, expressive character emotion, professional coloring, high resolution"
        })

    return {
        "title": title,
        "synopsis": synopsis,
        "genre": genre,
        "art_style": art_style,
        "character_name": hero,
        "character_visual_signature": visual_sig,
        "panels": panels
    }

async def generate_comic_story(
    prompt: str,
    character_name: str = "Hero",
    art_style: str = "Classic Comic Book",
    panel_count: int = 4
) -> Dict[str, Any]:
    """
    Invokes Google Gemini with elevated prompt engineering to craft a rich,
    emotionally engaging, realistic multi-panel comic book script with consistent character design.
    """
    api_key = config.GEMINI_API_KEY
    if not api_key:
        logger.info("Using enhanced offline narrative engine for rich story generation.")
        return _generate_enhanced_story(prompt, character_name, art_style, panel_count)

    user_instructions = f"""
Write an exceptional, realistic, and deeply engaging {panel_count}-panel comic book story:
- User Premise: {prompt}
- Protagonist Name: {character_name or 'Hope'}
- Desired Visual Art Style: {art_style}
- Total Panels: {panel_count}

Strict Storytelling Rules:
1. **Title**: Punchy, memorable, and thematic (e.g., "Hope's Journey: The Whispering Woods").
2. **Character Visual Signature**: Define exact, consistent physical traits (clothing, colors, hair/fur, eyes, distinctive items) to repeat across all image prompts.
3. **Realistic Dramatic Arc**:
   - Panel 1: Compelling atmospheric hook, character vulnerability, and sensory setting.
   - Middle Panels: Genuine conflict, friction, setbacks, and rising tension.
   - Panel {panel_count}: High-stakes climax, emotional breakthrough, or memorable heroic resolution.
4. **Dialogue**: Natural dialogue with subtext, personality, wit, or emotional honesty. Avoid cliché robotic sentences.
5. **Captions**: Atmospheric, literary narrative prose that captures mood and inner feelings.
6. **Sound Effects**: Dynamic, comic onomatopoeia (e.g. POW!, WHOOSH!, SKRRRT!, RUMBLE!, SHHHK!).
7. **Image Prompts**: Extremely detailed prompts specifying character visual signature, camera angle (wide shot, Dutch angle, dramatic close-up, splash), environmental lighting, and the '{art_style}' style.
"""

    # Try official google.genai SDK with multi-model fallback sequence
    models_to_try = [config.TEXT_MODEL, "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest", "gemini-3.1-flash-lite"]
    seen = set()
    ordered_models = [m for m in models_to_try if m and not (m in seen or seen.add(m))]

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        for m in ordered_models:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=[SYSTEM_PROMPT, user_instructions],
                )
                if response and response.text:
                    cleaned = _clean_json_response(response.text)
                    data = json.loads(cleaned)
                    logger.info(f"Successfully generated comic story with Gemini model: {m}")
                    return data
            except Exception as e_m:
                logger.warning(f"Gemini model {m} attempt failed: {e_m}. Trying next candidate...")
    except Exception as e_new:
        logger.warning(f"google.genai setup failed: {e_new}. Trying legacy SDK...")

    # Fallback to legacy google.generativeai if available
    try:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=api_key)
        model = genai_legacy.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        response = model.generate_content(user_instructions)
        cleaned = _clean_json_response(response.text)
        return json.loads(cleaned)
    except Exception as e_legacy:
        logger.error(f"Gemini API calls failed: {e_legacy}. Using enhanced narrative engine.")
        return _generate_enhanced_story(prompt, character_name, art_style, panel_count)


async def enhance_story_prompt(
    prompt: str,
    character_name: str = "Hero",
    art_style: str = "Classic Comic Book"
) -> str:
    """Takes a brief user idea and expands it into an evocative, multi-dimensional comic book premise with rich sensory detail, atmosphere, stakes, and emotional drive."""
    api_key = config.GEMINI_API_KEY
    if api_key:
        models_to_try = [config.TEXT_MODEL, "gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-flash-latest", "gemini-3.1-flash-lite"]
        seen = set()
        ordered_models = [m for m in models_to_try if m and not (m in seen or seen.add(m))]

        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt_instruction = (
                f"You are a master comic book editor and creative director. "
                f"Transform this simple comic premise into a vivid, cinematic, high-stakes comic story idea "
                f"in 2-3 sentences. Focus on sensory atmosphere, protagonist motivation, conflict, and visual spectacle. "
                f"Premise: '{prompt}' | Protagonist: '{character_name}' | Art Style: '{art_style}'\n"
                f"Return ONLY the enhanced story premise text without extra commentary or quotes."
            )
            for m in ordered_models:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=[prompt_instruction]
                    )
                    if response and response.text and len(response.text.strip()) > 15:
                        return response.text.strip().strip('"')
                except Exception as e_m:
                    logger.warning(f"Model {m} enhancement attempt failed: {e_m}")
        except Exception as e:
            logger.warning(f"Gemini prompt enhancement failed: {e}. Using algorithmic enhancer.")

    # Algorithmic creative enhancement
    base = prompt.strip().rstrip(".")
    style_lower = art_style.lower()

    if "cyberpunk" in style_lower or "sci-fi" in style_lower:
        enhancements = [
            f"Under the blinding holographic billboards and rain-slicked towers of Neo-Veridia, {character_name} uncovers a forbidden chronos-fragment tied to: {base}. As biomechanical enforcers descend through the neon haze, every ticking second threatens to destabilize the neural network of the entire metropolis.",
            f"In the shadow of the orbital spires, {character_name} navigates a treacherous cyber-underworld sparked by: {base}. Armed with an experimental pulse blade and a fractured memory chip, the truth will cost more than credits—it demands absolute rebellion."
        ]
    elif "noir" in style_lower or "graphic novel" in style_lower:
        enhancements = [
            f"Beneath the rusted streetlamps of 1940s Manhattan where the rain never truly washes away the blood, {character_name} takes on a case nobody else would touch: {base}. With shadows closing in from both corrupt city hall and the mob catacombs, survival depends on shooting first and trusting nobody.",
            f"Midnight smells like wet asphalt, cheap tobacco, and danger. Weary investigator {character_name} tracks a dangerous trail born from: {base}. In a city ruled by chiaroscuro shadows and whispered betrayals, the light at the end of the tunnel is usually an oncoming locomotive."
        ]
    elif "manga" in style_lower or "anime" in style_lower:
        enhancements = [
            f"When ancient celestial seals shatter across the sky, {character_name} must unleash an untamed spiritual power triggered by: {base}. With rival warriors gathering on the horizon and time running out, a legendary showdown will decide the fate of both mortal and spirit realms!",
            f"Driven by an unbroken promise and fiery determination, {character_name} charges into an epic trial after encountering: {base}. Dynamic elemental clashes, blazing willpower, and the bonds of camaraderie are pushed to their ultimate limits!"
        ]
    else:  # Classic Comic Book / Fantasy / Pop Art
        enhancements = [
            f"In an age of miraculous wonders and lurking perils, {character_name} embarks on an unforgettable odyssey: {base}. Facing treacherous trials through enchanted territory and guided by an unbreakable sense of purpose, an extraordinary destiny unfolds panel by panel.",
            f"When a sudden cosmic anomaly shakes the foundation of the world, {character_name} springs into dynamic action: {base}. Bold heroics, breathtaking splash-page spectacle, and heart-pounding courage collide in this classic adventure!"
        ]

    import hashlib
    idx = int(hashlib.md5(f"{base}_{character_name}".encode()).hexdigest(), 16) % len(enhancements)
    return enhancements[idx]

