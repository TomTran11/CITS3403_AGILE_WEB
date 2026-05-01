QUIZZES = {
    "social_energy": {
        "quiz_name": "Social Energy",
        "type": "category",
        "description": "Measures if a user is more introvert or extrovert.",
        "questions": [
            {
                "question_index": 1,
                "text": "I enjoy large social gatherings.",
                "reverse_scored": False
            },
            {
                "question_index": 2,
                "text": "I like meeting new people frequently.",
                "reverse_scored": False
            },
            {
                "question_index": 3,
                "text": "I feel energised after spending time with others.",
                "reverse_scored": False
            },
            {
                "question_index": 4,
                "text": "I enjoy spontaneous social plans.",
                "reverse_scored": False
            },
            {
                "question_index": 5,
                "text": "I like being around people most of the time.",
                "reverse_scored": False
            },
            {
                "question_index": 6,
                "text": "I need alone time to recharge after socialising.",
                "reverse_scored": True
            },
            {
                "question_index": 7,
                "text": "I prefer one-on-one conversations over group settings.",
                "reverse_scored": True
            },
            {
                "question_index": 8,
                "text": "I feel drained after too much social interaction.",
                "reverse_scored": True
            },
            {
                "question_index": 9,
                "text": "I prefer quiet environments over busy social scenes.",
                "reverse_scored": True
            },
            {
                "question_index": 10,
                "text": "I usually avoid being the centre of attention.",
                "reverse_scored": True
            }
        ],
        "categories": [
            {"name": "introverted", "min_score": 10, "max_score": 19},
            {"name": "selectively_social", "min_score": 20, "max_score": 29},
            {"name": "ambivert", "min_score": 30, "max_score": 39},
            {"name": "extroverted", "min_score": 40, "max_score": 50}
        ]
    },

    "food_preferences": {
        "quiz_name": "Food Preferences",
        "type": "direct",
        "description": "Captures food likes and assigns searchable keywords.",
        "questions": [
            {
                "question_index": 1,
                "text": "I like spicy food.",
                "keyword": "spicy_lover",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 2,
                "text": "I enjoy cooking meals myself.",
                "keyword": "home_chef",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 3,
                "text": "I like trying new cuisines.",
                "keyword": "adventurous_eater",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 4,
                "text": "I enjoy eating out at restaurants or cafes.",
                "keyword": "dishes_avoider",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 5,
                "text": "I enjoy sweet foods and desserts.",
                "keyword": "sweet_treats",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 6,
                "text": "I prefer healthy food choices.",
                "keyword": "healthy_eating",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 7,
                "text": "I enjoy watching TV whilst I eat.",
                "keyword": "solo_eater",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 8,
                "text": "I like comfort foods and familiar meals.",
                "keyword": "comfort_eater",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 9,
                "text": "I enjoy fast food.",
                "keyword": "fast_foodie",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 10,
                "text": "I care a lot about food quality.",
                "keyword": "foodie",
                "assign_keyword_if_score_at_least": 4
            }
        ]
    },

    "cricket_knowledge": {
        "quiz_name": "Cricket Knowledge",
        "type": "category",
        "description": "Measures how much a user knows about cricket.",
        "questions": [
            {
                "question_index": 1,
                "text": "I know the difference between Test, ODI, and T20 cricket.",
                "reverse_scored": False
            },
            {
                "question_index": 2,
                "text": "I can name at least 5 current international cricket teams.",
                "reverse_scored": False
            },
            {
                "question_index": 3,
                "text": "I understand what LBW means in cricket.",
                "reverse_scored": False
            },
            {
                "question_index": 4,
                "text": "I follow cricket tournaments like the IPL or World Cup.",
                "reverse_scored": False
            },
            {
                "question_index": 5,
                "text": "I know who Sachin Tendulkar is.",
                "reverse_scored": False
            },
            {
                "question_index": 6,
                "text": "I find cricket too slow and boring to watch.",
                "reverse_scored": True
            },
            {
                "question_index": 7,
                "text": "I struggle to understand cricket scoring.",
                "reverse_scored": True
            },
            {
                "question_index": 8,
                "text": "I rarely watch or follow cricket matches.",
                "reverse_scored": True
            },
            {
                "question_index": 9,
                "text": "I don't know what a wicket is.",
                "reverse_scored": True
            },
            {
                "question_index": 10,
                "text": "Cricket rules confuse me.",
                "reverse_scored": True
            }
        ],
        "categories": [
            {"name": "cricket_novice", "min_score": 10, "max_score": 19},
            {"name": "casual_fan", "min_score": 20, "max_score": 29},
            {"name": "cricket_enthusiast", "min_score": 30, "max_score": 39},
            {"name": "cricket_expert", "min_score": 40, "max_score": 50}
        ]
    },

    "football_preferences": {
        "quiz_name": "Football Preferences",
        "type": "direct",
        "description": "Captures football interests and assigns searchable keywords.",
        "questions": [
            {
                "question_index": 1,
                "text": "I watch football matches regularly.",
                "keyword": "football_fan",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 2,
                "text": "I support a specific football club.",
                "keyword": "club_supporter",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 3,
                "text": "I enjoy playing football myself.",
                "keyword": "football_player",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 4,
                "text": "I follow international football tournaments like the World Cup.",
                "keyword": "international_football_fan",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 5,
                "text": "I enjoy watching football with friends or family.",
                "keyword": "social_football_watcher",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 6,
                "text": "I follow football transfer news and player stats.",
                "keyword": "football_analyst",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 7,
                "text": "I play fantasy football leagues.",
                "keyword": "fantasy_football_player",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 8,
                "text": "I enjoy attending live football matches.",
                "keyword": "live_football_attendee",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 9,
                "text": "I like discussing football tactics and strategies.",
                "keyword": "football_tactician",
                "assign_keyword_if_score_at_least": 4
            },
            {
                "question_index": 10,
                "text": "I watch football highlights and analysis shows.",
                "keyword": "football_analyst_viewer",
                "assign_keyword_if_score_at_least": 4
            }
        ]
    }
}