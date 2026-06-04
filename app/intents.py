# intents.py

INTENT_PHRASES = {
    # --- 3D Navigation Actions ---
    "NAVIGATE_PROJECTS": [
        "projects", "project", "show me your work", "what have you built", 
        "repositories", "portfolio", "my projects", "your projects", 
        "show projects", "open projects", "take me to projects", "go to projects", 
        "project section", "show portfolio", "open portfolio", "what have you made", 
        "your work", "recent projects", "featured projects", "development projects", "coding projects"
    ],
    "OPEN_RESUME": [
        "resume", "cv", "education", "experience", "show me the cv", 
        "show resume", "open resume", "view resume", "download resume", 
        "my resume", "your resume", "curriculum vitae", "professional profile", 
        "work experience", "academic background", "qualification", "career history", 
        "employment history", "show qualifications", "show experience"
    ],
    "NAVIGATE_SKILLS": [
        "skills", "tech stack", "languages", "what do you know", 
        "technical skills", "technologies", "programming languages", "frameworks", 
        "tools", "my skills", "your skills", "show skills", "open skills", 
        "go to skills", "skill section", "developer skills", "expertise", 
        "competencies", "technical expertise", "what technologies do you use"
    ],
    "NAVIGATE_SOCIAL": [
        "social", "social media", "social links", "social profiles", 
        "contact links", "github", "linkedin", "twitter", "instagram", 
        "connect with me", "find me online", "show social media", "open social media", 
        "go to social", "social section", "online profiles", "social accounts", 
        "my profiles", "contact me", "network profiles"
    ],
    "NAVIGATE_TIME": [
        "time lamp", "lamp", "clock", "time", "show time", 
        "current time", "digital clock", "open time lamp", "go to clock", 
        "time section", "what time is it", "display clock", "show clock", 
        "view time", "time widget", "open clock", "current clock"
    ],
    "NAVIGATE_GLOBE": [
        "globe", "travel globe", "travel", "world map", "map", 
        "locations", "places", "countries", "explore globe", "open globe", 
        "go to globe", "travel section", "show map", "show globe", "world", 
        "visited places", "travel history", "explore world", "interactive globe"
    ],
    "NAVIGATE_BOOKSHELF": [
        "bookshelf", "books", "library", "reading", "book collection", 
        "my books", "favorite books", "recommended books", "show bookshelf", 
        "open bookshelf", "go to bookshelf", "book section", "reading list", 
        "book recommendations", "library section", "what are you reading", 
        "show books", "view books"
    ],
    
    # --- Basic Greetings & Conversations ---
    "GREETING": [
        "hi", "hello", "hey", "yo", "good morning", "good afternoon", "sup", "whats up", "whatsapp"
    ],
    "ABOUT_PROJECT": [
        "what is this", "why this project", "explain this website", "what am i looking at", "tell me about this house"
    ],
    "ABOUT_CREATOR": [
        "who are you", "who am i talking to", "who made this", "who is the creator", "who am i"
    ]
}

INTENT_REPLIES = {
    # "NAVIGATE_PROJECTS": "Heading over to the projects area.",
    # "OPEN_RESUME": "Opening the resume.",
    # "NAVIGATE_SKILLS": "Checking out the tech stack and skills wall.",
    # "NAVIGATE_SOCIAL": "Checking out the Social media section.",
    # "NAVIGATE_TIME": "Checking out the time lamp.",
    # "NAVIGATE_GLOBE": "Going to the travel globe.",
    # "NAVIGATE_BOOKSHELF": "Checking the bookshelf.",
    
    # Conversational Responses
    "GREETING": "Hey there! Welcome to my interactive space. How can I guide you through the house?",
    "ABOUT_PROJECT": "This is 'MyLife Portfolio'—a 3D interactive portfolio built inside a virtual house to visualize my development journey, projects. In short it will contain all projects in my life.",
    "ABOUT_CREATOR": "You're exploring the space of a Computer Science and developer specializing in immersive 3D web applications and AI architectures."
}