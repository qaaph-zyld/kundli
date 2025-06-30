"""
Dasha Phala Data Module
Contains reference data for dasha phala (effects) in Vedic astrology.
"""

# Mahadasha effects based on classical references
MAHADASHA_EFFECTS = {
    "Su": {
        "general": "Sun Mahadasha generally brings authority, leadership, and government-related matters into focus.",
        "favorable": "When well-placed, brings political success, authority, fame, and good health.",
        "challenging": "When afflicted, may cause health issues related to heart, eyes, or bones, and conflicts with authority figures.",
        "classical_reference": "According to Brihat Parasara Hora Shastra (BPHS), 'The native will be wealthy, will have conveyances, be virtuous, be honoured by the king, will be famous and will enjoy many pleasures, if the Sun is in strength.'",
        "remedial_measures": "Worship of Lord Shiva, donation of wheat, jaggery, copper, and ruby on Sundays."
    },
    "Mo": {
        "general": "Moon Mahadasha relates to emotions, mind, mother, and public life.",
        "favorable": "When well-placed, brings emotional stability, popularity, good relations with women, and success in public dealings.",
        "challenging": "When afflicted, may cause emotional instability, water-related diseases, and issues with mother or maternal figures.",
        "classical_reference": "BPHS states, 'If the Moon is strong, the native will gain clothes, ornaments, conveyances, and happiness from women and will be wealthy and honoured by the king.'",
        "remedial_measures": "Worship of Goddess Parvati, donation of rice, silver, and pearls on Mondays."
    },
    "Ma": {
        "general": "Mars Mahadasha brings energy, courage, and matters related to land, property, and siblings.",
        "favorable": "When well-placed, brings courage, leadership in technical fields, property gains, and success in competitions.",
        "challenging": "When afflicted, may cause accidents, surgeries, conflicts, and blood-related diseases.",
        "classical_reference": "BPHS mentions, 'If Mars is strong, the native will be endowed with lands, conveyances, and wealth, will be honoured by the king and will be strong, valorous, and intelligent.'",
        "remedial_measures": "Worship of Lord Hanuman, donation of red lentils, copper, and coral on Tuesdays."
    },
    "Me": {
        "general": "Mercury Mahadasha relates to intelligence, communication, business, and education.",
        "favorable": "When well-placed, brings success in education, business, communication skills, and intellectual pursuits.",
        "challenging": "When afflicted, may cause speech problems, nervous disorders, and issues in business or education.",
        "classical_reference": "According to BPHS, 'If Mercury is strong, the native will get wealth, learning, and education, will have sons and friends, will be happy and will have good qualities.'",
        "remedial_measures": "Worship of Lord Vishnu, donation of green gram, emerald, and books on Wednesdays."
    },
    "Ju": {
        "general": "Jupiter Mahadasha relates to wisdom, spirituality, children, and higher education.",
        "favorable": "When well-placed, brings spiritual growth, higher education, children, wealth, and respect from society.",
        "challenging": "When afflicted, may cause issues related to children, liver problems, and excessive weight gain.",
        "classical_reference": "BPHS states, 'If Jupiter is strong, the native will be wealthy, learned in Shastras, honoured by the king, virtuous, and will enjoy happiness from sons and friends.'",
        "remedial_measures": "Worship of Lord Dattatreya, donation of yellow clothes, gold, and yellow sapphire on Thursdays."
    },
    "Ve": {
        "general": "Venus Mahadasha relates to marriage, relationships, luxury, arts, and comforts.",
        "favorable": "When well-placed, brings marital happiness, luxury, artistic talents, and pleasures of life.",
        "challenging": "When afflicted, may cause relationship problems, kidney issues, and excessive indulgence.",
        "classical_reference": "BPHS mentions, 'If Venus is strong, the native will be endowed with conveyances, ornaments, clothes, and happiness from wife and friends, and will be wealthy and honoured by the king.'",
        "remedial_measures": "Worship of Goddess Lakshmi, donation of white clothes, silver, and diamond on Fridays."
    },
    "Sa": {
        "general": "Saturn Mahadasha relates to longevity, discipline, hard work, and delays.",
        "favorable": "When well-placed, brings discipline, professional success through hard work, and spiritual growth.",
        "challenging": "When afflicted, may cause delays, obstacles, chronic diseases, and separation from loved ones.",
        "classical_reference": "According to BPHS, 'If Saturn is strong, the native will be endowed with wealth, grains, and happiness, will be learned in Shastras, and will be famous and strong.'",
        "remedial_measures": "Worship of Lord Hanuman, donation of black sesame seeds, iron, and blue sapphire on Saturdays."
    },
    "Ra": {
        "general": "Rahu Mahadasha relates to foreign influences, unconventional matters, and sudden changes.",
        "favorable": "When well-placed, brings foreign travel, unconventional success, and sudden gains.",
        "challenging": "When afflicted, may cause confusion, deception, and health issues related to poisoning or allergies.",
        "classical_reference": "BPHS states, 'Rahu gives effects similar to Saturn, but with more intensity and unpredictability.'",
        "remedial_measures": "Worship of Lord Ganesha, donation of goat, hessonite, and black clothes on Saturdays."
    },
    "Ke": {
        "general": "Ketu Mahadasha relates to spirituality, mysticism, and detachment.",
        "favorable": "When well-placed, brings spiritual growth, intuition, and success in occult sciences.",
        "challenging": "When afflicted, may cause sudden separations, accidents, and mysterious ailments.",
        "classical_reference": "BPHS mentions, 'Ketu gives effects similar to Mars, but with more focus on spiritual and mystical matters.'",
        "remedial_measures": "Worship of Lord Ganesha, donation of multicolored clothes, cat's eye, and pulses on Tuesdays."
    }
}

# Antardasha effects based on classical references
# This is a simplified version focusing on planet combinations
ANTARDASHA_EFFECTS = {
    "Su": {
        "Su": "Sun-Sun period may bring government recognition, but also health issues related to heat and inflammation.",
        "Mo": "Sun-Moon period brings emotional stability, mother's blessings, and public recognition.",
        "Ma": "Sun-Mars period brings energy, courage, and success in competitions, but watch for accidents.",
        "Me": "Sun-Mercury period brings success in education, communication skills, and intellectual pursuits.",
        "Ju": "Sun-Jupiter period brings spiritual growth, higher education, and respect from authority figures.",
        "Ve": "Sun-Venus period brings luxury, artistic talents, and pleasures, but possible conflicts in relationships.",
        "Sa": "Sun-Saturn period brings hard work, discipline, but also delays and obstacles from authority figures.",
        "Ra": "Sun-Rahu period brings foreign influences, unconventional success, but also possible deception.",
        "Ke": "Sun-Ketu period brings spiritual growth, but also sudden separations and health issues."
    },
    "Mo": {
        "Su": "Moon-Sun period brings emotional stability, recognition, and success in public life.",
        "Mo": "Moon-Moon period intensifies emotions, brings connection with mother, and public dealings.",
        "Ma": "Moon-Mars period brings energy, but emotional volatility and possible conflicts with women.",
        "Me": "Moon-Mercury period brings good communication, education, and business success.",
        "Ju": "Moon-Jupiter period brings emotional wisdom, spiritual growth, and blessings from mother.",
        "Ve": "Moon-Venus period brings happiness in relationships, luxury, and artistic talents.",
        "Sa": "Moon-Saturn period brings emotional discipline, but also possible depression and health issues.",
        "Ra": "Moon-Rahu period brings emotional confusion, foreign influences, and possible deception.",
        "Ke": "Moon-Ketu period brings spiritual growth, but also emotional detachment and health issues."
    },
    # Additional planet combinations follow the same pattern
    # Abbreviated for brevity
}

# Pratyantardasha effects - simplified version
# In practice, these would be more detailed and specific
PRATYANTARDASHA_EFFECTS = {
    # Simplified for brevity
    # Would follow similar pattern to antardasha effects but with more specific combinations
}

# House-based effects for dashas
HOUSE_BASED_EFFECTS = {
    1: "Effects related to self, personality, health, and overall life direction.",
    2: "Effects related to wealth, family, speech, and early education.",
    3: "Effects related to courage, siblings, short journeys, and communication.",
    4: "Effects related to mother, home, property, education, and emotional happiness.",
    5: "Effects related to children, creativity, intelligence, and speculative gains.",
    6: "Effects related to enemies, debts, diseases, and service.",
    7: "Effects related to spouse, business partnerships, foreign travel, and public relations.",
    8: "Effects related to longevity, obstacles, occult knowledge, and sudden events.",
    9: "Effects related to fortune, higher education, spirituality, and long journeys.",
    10: "Effects related to career, authority, father, and social status.",
    11: "Effects related to gains, elder siblings, friends, and fulfillment of desires.",
    12: "Effects related to expenses, losses, foreign residence, and spiritual liberation."
}

# Nakshatra-based effects for dashas
NAKSHATRA_EFFECTS = {
    "Ashwini": "Quick results, healing abilities, travel, and new beginnings.",
    "Bharani": "Struggle, endurance, transformation, and eventual success.",
    "Krittika": "Sharp intellect, leadership, but possible conflicts and separations.",
    "Rohini": "Growth, prosperity, creativity, and material comforts.",
    "Mrigashira": "Searching, exploration, travel, and intellectual pursuits.",
    "Ardra": "Storms, struggles, but also breakthroughs and transformations.",
    "Punarvasu": "Return, renewal, wealth, and domestic happiness.",
    "Pushya": "Nourishment, prosperity, spiritual growth, and success.",
    "Ashlesha": "Hidden knowledge, mysteries, healing, but also deception.",
    "Magha": "Power, authority, ancestral blessings, and leadership.",
    "Purva Phalguni": "Enjoyment, creativity, romance, and entertainment.",
    "Uttara Phalguni": "Social success, marriage, partnerships, and stability.",
    "Hasta": "Skills, healing, craftsmanship, and practical achievements.",
    "Chitra": "Recognition, beauty, arts, and creative expression.",
    "Swati": "Independence, travel, spiritual seeking, and adaptability.",
    "Vishakha": "Determination, focus, achievement, and purposeful action.",
    "Anuradha": "Friendship, cooperation, success through others, and balance.",
    "Jyeshtha": "Power, courage, leadership, but possible conflicts.",
    "Mula": "Destruction of old patterns, spiritual growth, and new foundations.",
    "Purva Ashadha": "Early victory, water-related matters, and invigoration.",
    "Uttara Ashadha": "Later victory, stability, and universal principles.",
    "Shravana": "Learning, wisdom, fame, and connection to higher knowledge.",
    "Dhanishta": "Wealth, music, generosity, and abundance.",
    "Shatabhisha": "Healing, occult knowledge, isolation, and breakthroughs.",
    "Purva Bhadrapada": "Spiritual fire, transformation, and mystical experiences.",
    "Uttara Bhadrapada": "Spiritual water, universal love, and final liberation.",
    "Revati": "Nourishment, prosperity, conclusion, and transition."
}
