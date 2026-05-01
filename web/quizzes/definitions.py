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

    "communication_style": {
        "quiz_name": "Communication Style",
        "type": "category",
        "description": "Discovers how you naturally prefer to communicate and connect with others.",
        "questions": [
            {
                "question_index": 1,
                "text": "I prefer to think things through before responding in a conversation.",
                "reverse_scored": True
            },
            {
                "question_index": 2,
                "text": "I feel comfortable expressing my emotions openly to people I've just met.",
                "reverse_scored": False
            },
            {
                "question_index": 3,
                "text": "I would rather send a voice message than type a long text.",
                "reverse_scored": False
            },
            {
                "question_index": 4,
                "text": "I find it easy to bring up difficult topics in a friendship.",
                "reverse_scored": False
            },
            {
                "question_index": 5,
                "text": "I prefer to check in with friends frequently rather than catch up occasionally.",
                "reverse_scored": False
            },
            {
                "question_index": 6,
                "text": "I enjoy deep one-on-one conversations more than group chats.",
                "reverse_scored": False
            },
            {
                "question_index": 7,
                "text": "I tend to use humour to connect with new people.",
                "reverse_scored": False
            },
            {
                "question_index": 8,
                "text": "I like to have a plan for what I'll talk about before social events.",
                "reverse_scored": True
            },
            {
                "question_index": 9,
                "text": "I often go quiet or withdraw when I feel overwhelmed in social settings.",
                "reverse_scored": True
            },
            {
                "question_index": 10,
                "text": "I find it easy to keep a conversation going with someone I just met.",
                "reverse_scored": False
            }
        ],
        "categories": [
            {"name": "Reserved",  "min_score": 0,  "max_score": 12},
            {"name": "Reflective", "min_score": 13, "max_score": 25},
            {"name": "Engaging",   "min_score": 26, "max_score": 38},
            {"name": "Expressive", "min_score": 39, "max_score": 50}
        ]
    },
}