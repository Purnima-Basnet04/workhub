import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
sys.path.insert(0, '/Users/purnimabasnet/Desktop/workhub')
django.setup()

from skills.models import Skill

# Skills list - Combined from both technical and non-technical
skills = [
    # Programming Languages
    "Python", "JavaScript", "TypeScript", "Java", "C", "C++", "C#", "Ruby", "Go", "Rust",
    "Swift", "Kotlin", "PHP", "Perl", "Scala", "R", "MATLAB", "Dart", "Elixir", "Haskell",
    
    # Web Development
    "HTML", "CSS", "React", "Angular", "Vue.js", "Svelte", "Django", "Flask", "FastAPI",
    "Express.js", "Node.js", "Spring", "ASP.NET", "Laravel", "Ruby on Rails", "Next.js", "Nuxt.js",
    
    # Frontend Frameworks & Libraries
    "Bootstrap", "Tailwind CSS", "Material UI", "Chakra UI", "Sass", "Less", "Webpack", "Vite",
    
    # Backend & API
    "REST API", "GraphQL", "gRPC", "WebSocket", "OAuth", "JWT", "AWS Lambda", "Serverless",
    
    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite", "Oracle",
    "Firebase", "Supabase", "Prisma", "Cassandra", "DynamoDB",
    
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins",
    "GitLab CI/CD", "GitHub Actions", "Nginx", "Apache", "Linux", "Bash", "PowerShell",
    
    # Data Science & ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras", "Pandas", "NumPy",
    "Scikit-learn", "Data Analysis", "Data Visualization", "Tableau", "Power BI", "NLP",
    
    # Mobile Development
    "React Native", "Flutter", "iOS Development", "Android Development", "Xamarin",
    
    # Tools & Version Control
    "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Jira", "Confluence", "VS Code",
    
    # Security
    "Cybersecurity", "Penetration Testing", "OWASP", "SSL/TLS", "Security Auditing",
    
    # Software Engineering
    "Microservices", "System Design", "Architecture", "CI/CD", "Testing", "Unit Testing",
    "Integration Testing", "Selenium", "Jest", "Pytest", "Debugging", "Performance Optimization",
    
    # SEO & Analytics
    "SEO", "Google Analytics", "Figma", "UI/UX Design",
    
    # Engineering
    "Electrical Engineering", "Mechanical Engineering", "Civil Engineering",
    "AutoCAD", "SolidWorks", "PLC Programming", "Embedded Systems", "Robotics", "IoT", "Hardware Troubleshooting",
    
    # Job Role - Frontend
    "Frontend Development", "Frontend Developer", "React.js", "Vue.js", "Angular", "HTML5", "CSS3",
    "Responsive Design", "Web Accessibility",
    
    # Job Role - Backend
    "Backend Development", "Backend Developer", "API Development", "Database Design",
    "Server Management", "Authentication", "Authorization", "Caching", "Message Queues",
    "RESTful Services",
    
    # Job Role - Full Stack
    "Full Stack Development", "Full Stack Developer", "MERN Stack", "MEAN Stack",
    "Django REST Framework",
    
    # Job Role - DevOps
    "DevOps", "DevOps Engineer", "Cloud Infrastructure", "Containerization", "Orchestration",
    "Infrastructure as Code", "Monitoring", "Logging", "Incident Response", "Automation",
    
    # Job Role - Data Science
    "Data Science", "Data Scientist", "Statistical Analysis", "Data Mining",
    "Feature Engineering", "Model Deployment",
    
    # Soft Skills
    "Team Leadership", "Project Management", "Agile", "Scrum", "Kanban", "Communication",
    "Problem Solving", "Critical Thinking", "Time Management", "Mentoring",
    
    # Business & Management
    "Business Analysis", "Product Management", "Operations Management", "Strategic Planning",
    "Financial Modeling", "Risk Management", "Supply Chain Management",
    "Human Resource Management", "Recruitment", "CRM", "Stakeholder Management",
    "Entrepreneurship", "Business Development",
    
    # Marketing & Sales
    "Digital Marketing", "Social Media Marketing", "Content Writing", "Copywriting",
    "Email Marketing", "Performance Marketing", "Affiliate Marketing",
    "Brand Management", "Market Research", "Sales Negotiation", "Lead Generation", "Customer Support",
    
    # Creative & Design
    "Graphic Design", "Adobe Photoshop", "Adobe Illustrator", "Adobe Premiere Pro",
    "Video Editing", "Motion Graphics", "Canva", "Branding", "Storyboarding", "Animation", "Logo Design",
    
    # Finance & Accounting
    "Accounting", "Bookkeeping", "Tally", "QuickBooks", "Financial Reporting",
    "Tax Preparation", "Budget Planning", "Auditing", "Investment Analysis", "Banking Operations",
    
    # Administrative
    "Data Entry", "Microsoft Excel", "Microsoft Word", "Microsoft PowerPoint",
    "Google Workspace", "Documentation", "Office Administration", "Virtual Assistance",
    
    # Language & Communication
    "English Proficiency", "Nepali Proficiency", "Translation", "Technical Writing",
    "Public Speaking", "Presentation Skills",
    
    # E-Commerce & Freelancing
    "Shopify", "WooCommerce", "Amazon Seller Central", "Dropshipping", "Freelancing",
    "Proposal Writing", "Upwork", "Fiverr", "E-commerce Management",
    
    # Education & Training
    "Teaching", "Curriculum Development", "Lesson Planning", "Tutoring",
    "Instructional Design", "E-learning Development",
    
    # Health & Wellness
    "First Aid", "Nursing Assistance", "Pharmacy Assistance", "Nutrition Planning",
    "Fitness Training", "Yoga Instruction",
    
    # Legal
    "Legal Research", "Contract Drafting", "Corporate Law", "Intellectual Property", "Compliance",
    
    # Hospitality & Tourism
    "Hotel Management", "Event Planning", "Travel Booking", "Customer Service",
    "Food & Beverage Management", "Tourism",
    
    # Agriculture
    "Farm Management", "Crop Production", "Agricultural Technology", "Soil Science", "Animal Husbandry",
    
]


# Add skills to database
count = 0
for s in skills:
    obj, created = Skill.objects.get_or_create(name=s, defaults={'is_active': True})
    if created:
        count += 1

print(f"Created {count} skills. Total: {Skill.objects.count()}")
