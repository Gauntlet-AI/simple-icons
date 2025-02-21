import json
from collections import OrderedDict

# Dictionary mapping companies to their industries
INDUSTRY_MAPPINGS = {
    ".ENV": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],
    ".NET": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],
    "/e/": ["Telecommunications", "Computer and Electronic Product Manufacturing"],
    "1.1.1.1": ["Telecommunications", "Data Processing, Hosting, and Related Services"],
    "1&1": ["Telecommunications", "Data Processing, Hosting, and Related Services"],
    "1001Tracklists": ["Broadcasting (except Internet)", "Other Information Services"],
    "1Panel": ["Data Processing, Hosting, and Related Services"],
    "1Password": ["Data Processing, Hosting, and Related Services", "Computer and Electronic Product Manufacturing"],
    "2FAS": ["Data Processing, Hosting, and Related Services", "Computer and Electronic Product Manufacturing"],
    "2K": ["Motion Picture and Sound Recording Industries", "Publishing Industries (except Internet)"],
    "30 seconds of code": ["Professional, Scientific, and Technical Services", "Educational Services"],
    "365 Data Science": ["Educational Services", "Professional, Scientific, and Technical Services"],
    "3M": ["Chemical Manufacturing", "Manufacturing", "Professional, Scientific, and Technical Services"],
    "42": ["Educational Services"],
    "4chan": ["Other Information Services"],
    "500px": ["Other Information Services", "Professional, Scientific, and Technical Services"],
    "99designs": ["Professional, Scientific, and Technical Services"],
    "Abbott": ["Chemical Manufacturing", "Health and Personal Care Stores"],
    "Abbvie": ["Chemical Manufacturing", "Professional, Scientific, and Technical Services"],
    "Accenture": ["Professional, Scientific, and Technical Services", "Management of Companies and Enterprises"],
    "Accusoft": ["Data Processing, Hosting, and Related Services", "Software Publishers"],
    "AccuWeather": ["Data Processing, Hosting, and Related Services", "Broadcasting (except Internet)"],
    "Acer": ["Computer and Electronic Product Manufacturing"],
    "Activision": ["Software Publishers", "Motion Picture and Sound Recording Industries"],
    "Adafruit": ["Computer and Electronic Product Manufacturing", "Electronic Shopping and Mail-Order Houses"],
    "AdBlock": ["Software Publishers", "Data Processing, Hosting, and Related Services"],
    "Adidas": ["Apparel Manufacturing", "Sporting Goods, Hobby, Musical Instrument, and Book Stores"],
    "Adobe": ["Software Publishers", "Professional, Scientific, and Technical Services"],
    "ADP": ["Professional, Scientific, and Technical Services", "Data Processing, Hosting, and Related Services"],
    "Adyen": ["Credit Intermediation and Related Activities", "Data Processing, Hosting, and Related Services"],
     "Adblock Plus": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Ad blocking software
    "addy.io": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Email forwarding service
    "AdGuard": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Ad blocking software
    "Adminer": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database management tool
    "AdonisJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Adroll": ["Professional, Scientific, and Technical Services", "Advertising Services"],  # Marketing platform
    "Advent Of Code": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Programming challenges
    "Aegis Authenticator": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Authentication app
    "Aer Lingus": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Aeroflot": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Aeroméxico": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Aerospike": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database software
    "AEW": ["Performing Arts, Spectator Sports, and Related Industries", "Entertainment"],  # Wrestling promotion
    "AFDIAN": ["Data Processing, Hosting, and Related Services", "Financial Services"],  # Crowdfunding platform
    "AFFiNE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Knowledge management
    "Affinity": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Creative software suite
    "Affinity Designer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design software
    "Affinity Photo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Photo editing software
    "Affinity Publisher": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Publishing software
    "Afterpay": ["Credit Intermediation and Related Activities", "Financial Services"],  # Payment service
    "AfterShip": ["Data Processing, Hosting, and Related Services", "Support Activities for Transportation"],  # Shipping tracking
    "Agora": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Real-time communication platform
    "AI Dungeon": ["Software Publishers", "Entertainment"],  # AI text adventure game
    "AIB": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "AIOHTTP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "ACM": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Professional computing organization
    "ActiGraph": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Health monitoring devices
    "ActivityPub": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Social networking protocol
    "Actix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Actual Budget": ["Software Publishers", "Financial Services"],  # Budgeting software
    "Acura": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Automobile manufacturer,
    "Aiqfome": ["Data Processing, Hosting, and Related Services", "Food Services and Drinking Places"],  # Food delivery platform
    "Air Canada": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Air China": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Air France": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Air India": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Air Serbia": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Air Transat": ["Air Transportation", "Passenger Airlines"],  # Airline
    "AirAsia": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Airbnb": ["Data Processing, Hosting, and Related Services", "Accommodation"],  # Lodging platform
    "Airbrake": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Error tracking
    "Airbus": ["Transportation Equipment Manufacturing", "Aerospace Manufacturing"],  # Aircraft manufacturer
    "Airbyte": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data integration
    "Aircall": ["Telecommunications", "Software Publishers"],  # Cloud phone system
    "AirPlay Audio": ["Software Publishers", "Broadcasting Equipment"],  # Audio streaming protocol
    "AirPlay Video": ["Software Publishers", "Broadcasting Equipment"],  # Video streaming protocol
    "Airtable": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Collaborative platform
    "Airtel": ["Telecommunications", "Internet Service Providers"],  # Telecom provider
    "Ajv": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JSON Schema validator
    "Akamai": ["Data Processing, Hosting, and Related Services", "Telecommunications"],  # CDN provider
    "Akasa Air": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Akaunting": ["Software Publishers", "Financial Services"],  # Accounting software
    "Akiflow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Productivity software
    "Alacritty": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal emulator
    "Alamy": ["Professional, Scientific, and Technical Services", "Stock Photography"],  # Stock photo platform
    "Albert Heijn": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Alby": ["Software Publishers", "Financial Technology"],  # Bitcoin payments
    "Alchemy": ["Software Publishers", "Blockchain Technology"],  # Blockchain platform
    "Aldi Nord": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Aldi Süd": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Alfa Romeo": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Automobile manufacturer
    "Alfred": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Productivity software
    "Algolia": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Search API
    "Algorand": ["Financial Technology", "Blockchain Technology"],  # Blockchain platform
    "Alibaba Cloud": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud services
    "Alibaba.com": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # E-commerce
    "Alienware": ["Computer and Electronic Product Manufacturing", "Gaming Hardware"],  # Gaming computers
    "AliExpress": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # E-commerce
    "Alipay": ["Credit Intermediation and Related Activities", "Financial Technology"],  # Payment platform
    "Allegro": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # E-commerce
    "AlliedModders": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game modding
    "AlloCiné": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Movie database
    "AllTrails": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Hiking app
    "AlmaLinux": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Alpine Linux": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Alpine.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript framework
    "AlternativeTo": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Software directory
    "Alteryx": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Analytics software
    "Altium Designer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # PCB design software
    "Alwaysdata": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Web hosting
    "ALX": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Tech education
    "Amazon": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # E-commerce & tech
    "Amazon Alexa": ["Computer and Electronic Product Manufacturing", "Software Publishers"],  # Voice assistant
    "Amazon API Gateway": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # API management
    "Amazon CloudWatch": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Monitoring service
    "Amazon Cognito": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Authentication service
    "Amazon DocumentDB": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Database service
    "Amazon DynamoDB": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Database service
    "Amazon EC2": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud computing
    "Amazon ECS": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Container service
    "Amazon EKS": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Container service
    "Amazon ElastiCache": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Caching service
    "Amazon Fire TV": ["Computer and Electronic Product Manufacturing", "Broadcasting Equipment"],  # Streaming device
    "Amazon Games": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game publishing
    "Amazon Identity Access Management": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Security service
    "Amazon Lumberyard": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Amazon Luna": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Cloud gaming
    "Amazon Music": ["Data Processing, Hosting, and Related Services", "Broadcasting (except Internet)"],  # Music streaming
    "Amazon Pay": ["Credit Intermediation and Related Activities", "Financial Technology"],  # Payment service
    "Amazon Prime": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # Subscription service
    "Amazon RDS": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Database service
    "Amazon Redshift": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Data warehouse
    "Amazon Route 53": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # DNS service
    "Amazon S3": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Storage service
    "Amazon Simple Email Service": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Email service
    "Amazon SQS": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Message queue
    "Amazon Web Services": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "AMD": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor company
    "Ameba": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Blogging platform
    "American Airlines": ["Air Transportation", "Passenger Airlines"],  # Airline
    "American Express": ["Credit Intermediation and Related Activities", "Financial Services"],  # Financial services
    "AMG": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Luxury vehicle manufacturer
    "AMP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web component framework
    "Amul": ["Food Manufacturing", "Dairy Product Manufacturing"],  # Dairy company
    "ANA": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Anaconda": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Python distribution
    "Analogue": ["Computer and Electronic Product Manufacturing", "Gaming Hardware"],  # Gaming hardware
    "Andela": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Tech talent network
    "Android": ["Software Publishers", "Operating Systems"],  # Mobile operating system
    "Android Auto": ["Software Publishers", "Motor Vehicle Manufacturing"],  # Car software platform
    "Android Studio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development IDE
    "Angular": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "AniList": ["Internet Publishing and Broadcasting", "Entertainment"],  # Anime/manga database
    "Animal Planet": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # TV channel
    "AnkerMake": ["Computer and Electronic Product Manufacturing", "3D Printing"],  # 3D printer manufacturer
    "Anki": ["Software Publishers", "Educational Services"],  # Learning software
    "Ansible": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IT automation
    "Answer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Q&A platform
    "Ansys": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Engineering simulation
    "Ant Design": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design system
    "Anta": ["Apparel Manufacturing", "Sporting Goods, Hobby, Musical Instrument, and Book Stores"],  # Sportswear
    "Antena 3": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # TV channel
    "Anthropic": ["Professional, Scientific, and Technical Services", "Artificial Intelligence"],  # AI research
    "AntV": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data visualization
    "Anycubic": ["Computer and Electronic Product Manufacturing", "3D Printing"],  # 3D printer manufacturer
    "AnyDesk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Remote desktop
    "Anytype": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Knowledge management
    "AOL": ["Data Processing, Hosting, and Related Services", "Internet Publishing and Broadcasting"],  # Internet services
    "Apache": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software foundation
    "Apache Airflow": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Workflow management
    "Apache Ant": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Apache Cassandra": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Apache CloudStack": ["Software Publishers", "Cloud Computing"],  # Cloud platform
    "Apache Cordova": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mobile development
    "Apache CouchDB": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Apache DolphinScheduler": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Workflow platform
    "Apache Druid": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Analytics database
    "Apache ECharts": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Visualization library
    "Apache Flink": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Stream processing
    "Apache FreeMarker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Template engine
    "Apache Groovy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Apache Guacamole": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Remote access
    "Apache Hadoop": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Big data platform
    "Apache HBase": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Apache Hive": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data warehouse
    "Apache JMeter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Performance testing
    "Apache Kafka": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Stream processing
    "Apache Kylin": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Analytics platform
    "Apache Lucene": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Search engine
    "Apache Maven": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Apache NetBeans IDE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development IDE
    "Apache NiFi": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data integration
    "Apache OpenOffice": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Office suite
    "Apache Parquet": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data format
    "Apache Pulsar": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Messaging system
    "Apache RocketMQ": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Message broker
    "Apache Solr": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Search platform
    "Apache Spark": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Analytics engine
    "Apache Storm": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Stream processing
    "Apache Superset": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data visualization
    "Apache Tomcat": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Application server
    "Aparat": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Video platform
    "Apifox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API development
    "APM Terminals": ["Support Activities for Transportation", "Marine Cargo Handling"],  # Port operations
    "Apollo GraphQL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GraphQL platform
    "Apostrophe": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "App Store": ["Software Publishers", "Electronic Shopping and Mail-Order Houses"],  # App marketplace
    "AppGallery": ["Software Publishers", "Electronic Shopping and Mail-Order Houses"],  # App marketplace
    "Appian": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business process automation
    "Appium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Apple": ["Computer and Electronic Product Manufacturing", "Software Publishers"],  # Technology company
    "Apple Arcade": ["Software Publishers", "Entertainment"],  # Gaming service
    "Apple Music": ["Data Processing, Hosting, and Related Services", "Broadcasting (except Internet)"],  # Music streaming
    "Apple News": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # News service
    "Apple Pay": ["Credit Intermediation and Related Activities", "Financial Technology"],  # Payment service
    "Apple Podcasts": ["Internet Publishing and Broadcasting", "Broadcasting (except Internet)"],  # Podcast platform
    "Apple TV": ["Broadcasting (except Internet)", "Computer and Electronic Product Manufacturing"],  # Streaming platform
    "AppSignal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Application monitoring
    "Appsmith": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Internal tools platform
    "AppVeyor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Appwrite": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Backend platform
    "Aqua": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security platform
    "ARAL": ["Gasoline Stations", "Retail Trade"],  # Gas station chain
    "ArangoDB": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Arc": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "ArcGIS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GIS software
    "Arch Linux": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Archicad": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Architecture software
    "Archive of Our Own": ["Internet Publishing and Broadcasting", "Other Information Services"],  # Fan fiction archive
    "Ardour": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Audio workstation
    "Arduino": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Electronics platform
    "Argo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container orchestration
    "Argos": ["Department Stores", "Retail Trade"],  # Retail chain
    "Ariakit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI component library
    "ARK Ecosystem": ["Financial Technology", "Blockchain Technology"],  # Blockchain platform
    "Arlo": ["Computer and Electronic Product Manufacturing", "Security Systems"],  # Security systems
    "Arm": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Chip design
    "Arm Keil": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "Ars Technica": ["Internet Publishing and Broadcasting", "Other Information Services"],  # Tech news
    "Artifact Hub": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package registry
    "Artix Linux": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "ArtStation": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Art platform
    "arXiv": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Research repository
    "Asahi Linux": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Asana": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Asciidoctor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Document processor
    "asciinema": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal recorder
    "ASDA": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Aseprite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Pixel art tool
    "AssemblyScript": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Asterisk": ["Software Publishers", "Telecommunications"],  # VoIP platform
    "Aston Martin": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Luxury car manufacturer
    "Astra": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # WordPress theme
    "Astral": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Astro": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "ASUS": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Computer hardware
    "AT&T": ["Telecommunications", "Internet Service Providers"],  # Telecom provider
    "Atari": ["Software Publishers", "Computer and Electronic Product Manufacturing"],  # Gaming company
    "AtlasOS": ["Software Publishers", "Operating Systems"],  # Operating system
    "Atlassian": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "Auchan": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "Audacity": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Audio editor
    "Audi": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Audible": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Audiobook platform
    "Audio-Technica": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "Audiobookshelf": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Audiobook server
    "Audioboom": ["Internet Publishing and Broadcasting", "Broadcasting (except Internet)"],  # Podcast platform
    "Audiomack": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Music platform
    "Aurelia": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Auth0": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Authentication platform
    "Authelia": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Authentication server
    "Authentik": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Identity management
    "Authy": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Authentication app
    "AutoCAD": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CAD software
    "AutoCannon": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Benchmarking tool
    "Autodesk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design software
    "Autodesk Maya": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D animation
    "Autodesk Revit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # BIM software
    "AutoHotkey": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation software
    "AutoIt": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation software
    "Automattic": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Web platform company
    "Autoprefixer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS tool
    "AutoZone": ["Motor Vehicle and Parts Dealers", "Retail Trade"],  # Auto parts retailer
    "avajs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Avast": ["Software Publishers", "Computer Systems Design"],  # Security software
    "avianca": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Avira": ["Software Publishers", "Computer Systems Design"],  # Security software
    "Awesome Lists": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Resource curation
    "awesomeWM": ["Software Publishers", "Operating Systems"],  # Window manager
    "AWS Amplify": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Development platform
    "AWS Elastic Load Balancing": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Load balancer
    "AWS Fargate": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Container service
    "AWS Lambda": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Serverless computing
    "AWS Organizations": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Account management
    "AWS Secrets Manager": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Secrets management
    "Awwwards": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Web awards
    "Axios": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # HTTP client
    "B&R Automation": ["Computer and Electronic Product Manufacturing", "Industrial Automation"],  # Industrial automation
    "Babel": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript compiler
    "Babelio": ["Internet Publishing and Broadcasting", "Other Information Services"],  # Book community
    "Babylon.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D engine
    "Backblaze": ["Data Processing, Hosting, and Related Services", "Cloud Storage"],  # Cloud storage
    "Backbone": ["Computer and Electronic Product Manufacturing", "Gaming Hardware"],  # Gaming controller
    "Backbone.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript framework
    "Backendless": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Backend platform
    "Backstage": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Developer portal
    "Badoo": ["Data Processing, Hosting, and Related Services", "Social Networking Services"],  # Dating app
    "Baidu": ["Data Processing, Hosting, and Related Services", "Internet Publishing and Broadcasting"],  # Search engine
    "Bakaláři": ["Software Publishers", "Educational Services"],  # School management
    "Bamboo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Bambu Lab": ["Computer and Electronic Product Manufacturing", "3D Printing"],  # 3D printer manufacturer
    "Bandcamp": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Music platform
    "BandLab": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Music creation
    "Bandsintown": ["Data Processing, Hosting, and Related Services", "Entertainment"],  # Concert platform
    "Bank of America": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "Barclays": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "Baremetrics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Barmenia": ["Insurance Carriers and Related Activities", "Financial Services"],  # Insurance
    "Basecamp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Baserow": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database platform
    "Basic Attention Token": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "Bastyon": ["Software Publishers", "Social Networking Services"],  # Social platform
    "bat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code viewer
    "Bata": ["Footwear Manufacturing", "Clothing and Clothing Accessories Stores"],  # Shoe manufacturer
    "Battle.net": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Gaming platform
    "Bazel": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build system
    "Beatport": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Music store
    "Beats": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data shipper
    "Beats by Dre": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "BeatStars": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Music marketplace
    "Beekeeper Studio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database tool
    "Behance": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Creative platform
    "Beijing Subway": ["Transit and Ground Passenger Transportation", "Public Transportation"],  # Transit system
    "BEM": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS methodology
    "Bentley": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Bento": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Profile platform
    "BentoBox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Restaurant platform
    "BentoML": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML deployment
    "BeReal": ["Software Publishers", "Social Networking Services"],  # Social media
    "Betfair": ["Gambling Industries", "Data Processing, Hosting, and Related Services"],  # Betting platform
    "Better Stack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "BetterDiscord": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Discord mod
    "Bevy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Big Cartel": ["Data Processing, Hosting, and Related Services", "Electronic Shopping and Mail-Order Houses"],  # E-commerce platform
    "bigbasket": ["Electronic Shopping and Mail-Order Houses", "Food and Beverage Stores"],  # Online grocery
    "BigBlueButton": ["Software Publishers", "Educational Services"],  # Video conferencing
    "BigCommerce": ["Software Publishers", "Electronic Shopping and Mail-Order Houses"],  # E-commerce platform
    "Bilibili": ["Internet Publishing and Broadcasting", "Entertainment"],  # Video platform
    "Billboard": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Music media
    "BIM": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Binance": ["Financial Technology", "Cryptocurrency Exchange"],  # Crypto exchange
    "Bio Link": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Link platform
    "Biome": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "BisectHosting": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Game hosting
    "Bit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Component platform
    "Bitbucket": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code hosting
    "Bitcoin": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "Bitcoin Cash": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "Bitcoin SV": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "BitComet": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Torrent client
    "Bitdefender": ["Software Publishers", "Computer Systems Design"],  # Security software
    "Bitly": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Link shortener
    "Bitrise": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "BitTorrent": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # File sharing
    "Bitwarden": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Password manager
    "Bitwig": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Music production
    "Blackberry": ["Computer and Electronic Product Manufacturing", "Telecommunications"],  # Mobile devices
    "Blackmagic Design": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Video equipment
    "Blazemeter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Performance testing
    "Blazor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Blender": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D software
    "Blockbench": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D modeling
    "Blockchain.com": ["Financial Technology", "Blockchain Technology"],  # Crypto platform
    "Blogger": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Blogging platform
    "Bloglovin": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Blog aggregator
    "Blueprint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Bluesky": ["Software Publishers", "Social Networking Services"],  # Social network
    "Bluesound": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "Bluetooth": ["Computer and Electronic Product Manufacturing", "Wireless Technology"],  # Wireless standard
    "BMC Software": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Enterprise software
    "BMW": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "BNB Chain": ["Financial Technology", "Blockchain Technology"],  # Blockchain platform
    "BoardGameGeek": ["Internet Publishing and Broadcasting", "Entertainment"],  # Board game community
    "boAt": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "Boehringer Ingelheim": ["Chemical Manufacturing", "Pharmaceutical Manufacturing"],  # Pharmaceutical company
    "Boeing": ["Transportation Equipment Manufacturing", "Aerospace Manufacturing"],  # Aircraft manufacturer
    "Bombardier": ["Transportation Equipment Manufacturing", "Aerospace Manufacturing"],  # Aircraft manufacturer
    "Bookalope": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Book production
    "BookBub": ["Internet Publishing and Broadcasting", "Electronic Shopping and Mail-Order Houses"],  # Book promotion
    "Bookmeter": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Book tracking
    "BookMyShow": ["Data Processing, Hosting, and Related Services", "Entertainment"],  # Event ticketing
    "BookStack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation platform
    "Boost": ["Telecommunications", "Wireless Carriers"],  # Mobile carrier
    "Boosty": ["Data Processing, Hosting, and Related Services", "Financial Technology"],  # Creator platform
    "Boots": ["Health and Personal Care Stores", "Retail Trade"],  # Pharmacy chain
    "Bootstrap": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "BorgBackup": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Backup software
    "Bosch": ["Computer and Electronic Product Manufacturing", "Manufacturing"],  # Industrial manufacturer
    "Bose": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "Botble CMS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Content management
    "boulanger": ["Electronics and Appliance Stores", "Retail Trade"],  # Electronics retailer
    "Bower": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Box": ["Data Processing, Hosting, and Related Services", "Cloud Storage"],  # Cloud storage
    "Boxy SVG": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # SVG editor
    "Braintree": ["Credit Intermediation and Related Activities", "Financial Technology"],  # Payment processing
    "Brandfolder": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Asset management
    "Brave": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "Breaker": ["Internet Publishing and Broadcasting", "Broadcasting (except Internet)"],  # Podcast platform
    "Brenntag": ["Chemical Manufacturing", "Wholesale Trade"],  # Chemical distribution
    "Brevo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Marketing platform
    "Brex": ["Credit Intermediation and Related Activities", "Financial Technology"],  # Financial services
    "Bricks": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "British Airways": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Broadcom": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor company
    "Bruno": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API client
    "BSD": ["Software Publishers", "Operating Systems"],  # Operating system
    "bspwm": ["Software Publishers", "Operating Systems"],  # Window manager
    "BT": ["Telecommunications", "Internet Service Providers"],  # Telecom provider
    "Buddy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Budibase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Low-code platform
    "Buefy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI components
    "Buffer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Social media management
    "Bugatti": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Bugcrowd": ["Professional, Scientific, and Technical Services", "Cybersecurity"],  # Security platform
    "Bugsnag": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Error monitoring
    "Buhl": ["Software Publishers", "Financial Services"],  # Financial software
    "Buildkite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "BuiltByBit": ["Electronic Shopping and Mail-Order Houses", "Software Publishers"],  # Software marketplace
    "Bukalapak": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # E-commerce
    "Bulma": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS framework
    "Bun": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript runtime
    "Bungie": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game developer
    "bunq": ["Credit Intermediation and Related Activities", "Financial Technology"],  # Digital banking
    "Burger King": ["Food Services and Drinking Places", "Restaurants"],  # Fast food
    "Burp Suite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security testing
    "Burton": ["Apparel Manufacturing", "Sporting Goods, Hobby, Musical Instrument, and Book Stores"],  # Snowboard equipment
    "Buy Me A Coffee": ["Data Processing, Hosting, and Related Services", "Financial Technology"],  # Creator platform
    "BuySellAds": ["Professional, Scientific, and Technical Services", "Advertising Services"],  # Ad network
    "BuzzFeed": ["Internet Publishing and Broadcasting", "Other Information Services"],  # Digital media
    "BVG": ["Transit and Ground Passenger Transportation", "Public Transportation"],  # Transit authority
    "Byju's": ["Educational Services", "Software Publishers"],  # Educational technology
    "ByteDance": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Tech company
    "C": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "C++": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "C++ Builder": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development IDE
    "Cachet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Status page system
    "Caddy": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Web server
    "Cadillac": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "CafePress": ["Electronic Shopping and Mail-Order Houses", "Printing and Related Support Activities"],  # Custom merchandise
    "Cairo Graphics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics library
    "Cairo Metro": ["Transit and Ground Passenger Transportation", "Public Transportation"],  # Transit system
    "CaixaBank": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "CakePHP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Cal.com": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Scheduling platform
    "Calibre-Web": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # E-book manager
    "Campaign Monitor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email marketing
    "Camunda": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Process automation
    "Canonical": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software company
    "Canva": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design platform
    "Canvas": ["Software Publishers", "Educational Services"],  # Learning management
    "Capacitor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # App platform
    "CapRover": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # PaaS platform
    "Car Throttle": ["Internet Publishing and Broadcasting", "Motor Vehicle Information"],  # Automotive media
    "Cardano": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "Carlsberg Group": ["Beverage Manufacturing", "Breweries"],  # Brewery
    "Carrd": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "Carrefour": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "Carto": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping platform
    "Cash App": ["Financial Technology", "Credit Intermediation and Related Activities"],  # Payment app
    "Castbox": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Podcast platform
    "Castorama": ["Building Material and Garden Equipment and Supplies Dealers", "Retail Trade"],  # Home improvement
    "Castro": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Podcast app
    "Caterpillar": ["Machinery Manufacturing", "Construction Machinery"],  # Heavy equipment
    "CBC": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # Broadcaster
    "CBS": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # Broadcaster
    "CCC": ["Professional, Scientific, and Technical Services", "Certification Services"],  # Certification body
    "CCleaner": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # System optimization
    "CD Projekt": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game developer
    "CE": ["Professional, Scientific, and Technical Services", "Certification Services"],  # Certification mark
    "Celery": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Task queue
    "Celestron": ["Computer and Electronic Product Manufacturing", "Optical Equipment"],  # Telescope manufacturer
    "CentOS": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Ceph": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Storage platform
    "Cesium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D mapping
    "Chai": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Chainguard": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security platform
    "Chainlink": ["Financial Technology", "Blockchain Technology"],  # Blockchain oracle
    "Chakra UI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Channel 4": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # Broadcaster
    "Charles": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Proxy software
    "Chart.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Charting library
    "ChartMogul": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Chase": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "ChatBot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat platform
    "Chatwoot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Customer engagement
    "CheckiO": ["Educational Services", "Software Publishers"],  # Coding platform
    "Checkmarx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security testing
    "Checkmk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring
    "Chedraui": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "Cheerio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web scraping
    "Chef": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Infrastructure automation
    "Chemex": ["Manufacturing", "Household Appliances"],  # Coffee maker
    "Chess.com": ["Internet Publishing and Broadcasting", "Entertainment"],  # Chess platform
    "Chevrolet": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Chia Network": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "China Eastern Airlines": ["Air Transportation", "Passenger Airlines"],  # Airline
    "China Southern Airlines": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Chocolatey": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Chromatic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI testing
    "Chrome Web Store": ["Software Publishers", "Electronic Shopping and Mail-Order Houses"],  # App store
    "Chromecast": ["Computer and Electronic Product Manufacturing", "Broadcasting Equipment"],  # Streaming device
    "Chrysler": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Chupa Chups": ["Food Manufacturing", "Confectionery Manufacturing"],  # Candy manufacturer
    "Cilium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Network software
    "Cinema 4D": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D software
    "Cinnamon": ["Software Publishers", "Operating Systems"],  # Desktop environment
    "Circle": ["Financial Technology", "Credit Intermediation and Related Activities"],  # Financial services
    "CircleCI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "CircuitVerse": ["Software Publishers", "Educational Services"],  # Circuit simulator
    "Cirrus CI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI platform
    "Cisco": ["Computer and Electronic Product Manufacturing", "Telecommunications"],  # Network equipment
    "Citrix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Virtualization
    "Citroën": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "CiviCRM": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CRM software
    "Civo": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "Clarifai": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # AI platform
    "Claris": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "Clarivate": ["Professional, Scientific, and Technical Services", "Data Analytics"],  # Analytics company
    "Claude": ["Software Publishers", "Artificial Intelligence"],  # AI assistant
    "Clerk": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Authentication platform
    "Clever Cloud": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "ClickHouse": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "ClickUp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "CLion": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development IDE
    "Clockify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Time tracking
    "Clojure": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Cloud 66": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # DevOps platform
    "Cloud Foundry": ["Software Publishers", "Cloud Computing"],  # PaaS platform
    "CloudBees": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # DevOps platform
    "CloudCannon": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # CMS platform
    "Cloudera": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data platform
    "Cloudflare": ["Data Processing, Hosting, and Related Services", "Telecommunications"],  # Internet services
    "Cloudflare Pages": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Web hosting
    "Cloudflare Workers": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Serverless platform
    "Cloudinary": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Media management
    "Cloudron": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Server platform
    "Cloudsmith": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Package management
    "Cloudways": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Hosting platform
    "Clubforce": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Sports platform
    "Clubhouse": ["Software Publishers", "Social Networking Services"],  # Social audio
    "Clyp": ["Internet Publishing and Broadcasting", "Data Processing, Hosting, and Related Services"],  # Audio sharing
    "CMake": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build system
    "CNCF": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Tech foundation
    "CNES": ["Professional, Scientific, and Technical Services", "Aerospace"],  # Space agency
    "CNET": ["Internet Publishing and Broadcasting", "Other Information Services"],  # Tech news
    "CNN": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # News network
    "Co-op": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "Coca-Cola": ["Beverage Manufacturing", "Food Manufacturing"],  # Beverage company
    "Cockpit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Server management
    "Cockroach Labs": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database company
    "CocoaPods": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Cocos": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Coda": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Document platform
    "Codacy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "Code Climate": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "Code::Blocks": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development IDE
    "Codeberg": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code hosting
    "Codecademy": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "CodeceptJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "CodeChef": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding platform
    "Codecov": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code coverage
    "CodeCrafters": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "CodeFactor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "Codeforces": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding platform
    "Codefresh": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "CodeIgniter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Codeium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code completion
    "Codemagic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Codementor": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Mentoring platform
    "CodeMirror": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "CodeNewbie": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning community
    "CodePen": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code playground
    "CodeProject": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer community
    "Coder": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "CodersRank": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Developer platform
    "Coderwall": ["Professional, Scientific, and Technical Services", "Social Networking Services"],  # Developer network
    "CodeSandbox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code playground
    "Codeship": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "CodeSignal": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Technical assessment
    "CodeStream": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Developer collaboration
    "Codewars": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding challenges
    "Coding Ninjas": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding education
    "CodinGame": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding platform
    "Codio": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "CoffeeScript": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Coggle": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mind mapping
    "Cognizant": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "cohost": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social platform
    "Coinbase": ["Financial Technology", "Credit Intermediation and Related Activities"],  # Crypto exchange
    "CoinMarketCap": ["Financial Technology", "Data Processing, Hosting, and Related Services"],  # Crypto data
    "Collabora Online": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Office suite
    "ComicFury": ["Internet Publishing and Broadcasting", "Entertainment"],  # Comic hosting
    "comma": ["Computer and Electronic Product Manufacturing", "Motor Vehicle Manufacturing"],  # Autonomous driving
    "Commerzbank": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "commitlint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Commodore": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Computer manufacturer
    "Common Lisp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Common Workflow Language": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Workflow standard
    "Compiler Explorer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Composer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "CompTIA": ["Educational Services", "Professional, Scientific, and Technical Services"],  # IT certification
    "Comsol": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Simulation software
    "Conan": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Concourse": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Conda-Forge": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package repository
    "Conekta": ["Financial Technology", "Credit Intermediation and Related Activities"],  # Payment platform
    "Confluence": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Collaboration software
    "Construct 3": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Consul": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Service mesh
    "Contabo": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud provider
    "Contactless Payment": ["Financial Technology", "Credit Intermediation and Related Activities"],  # Payment technology
    "containerd": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container runtime
    "Contao": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Contentful": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Content platform
    "Contentstack": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Content platform
    "Continente": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "Contributor Covenant": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Code of conduct
    "Conventional Commits": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Git standard
    "Convertio": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # File conversion
    "Cookiecutter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project templates
    "Cooler Master": ["Computer and Electronic Product Manufacturing", "Computer Equipment"],  # PC components
    "Copa Airlines": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Coppel": ["Department Stores", "Retail Trade"],  # Retail chain
    "Cora": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "CorelDRAW": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design software
    "Corona Engine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Corona Renderer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Rendering engine
    "Corsair": ["Computer and Electronic Product Manufacturing", "Computer Equipment"],  # PC components
    "Couchbase": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Counter-Strike": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Video game
    "CountingWorks PRO": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "Coursera": ["Educational Services", "Internet Publishing and Broadcasting"],  # Learning platform
    "Coveralls": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code coverage
    "Coze": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # AI platform
    "cPanel": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Hosting control panel
    "Craft CMS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Craftsman": ["Manufacturing", "Tools Manufacturing"],  # Tool manufacturer
    "CrateDB": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Crayon": ["Professional, Scientific, and Technical Services", "Software Licensing"],  # Software management
    "Creality": ["Computer and Electronic Product Manufacturing", "3D Printing"],  # 3D printer manufacturer
    "Create React App": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Creative Commons": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Licensing
    "Creative Technology": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "Credly": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Digital badges
    "Crehana": ["Educational Services", "Internet Publishing and Broadcasting"],  # Learning platform
    "Crew United": ["Professional, Scientific, and Technical Services", "Entertainment"],  # Film industry network
    "CrewAI": ["Software Publishers", "Artificial Intelligence"],  # AI framework
    "Critical Role": ["Motion Picture and Sound Recording Industries", "Entertainment"],  # Entertainment company
    "Crowdin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Translation platform
    "Crowdsource": ["Professional, Scientific, and Technical Services", "Data Processing, Hosting, and Related Services"],  # Crowdsourcing
    "Crunchbase": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Company database
    "Crunchyroll": ["Internet Publishing and Broadcasting", "Entertainment"],  # Anime streaming
    "CRYENGINE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Cryptomator": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Encryption software
    "CryptPad": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Collaboration platform
    "Crystal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "CSDN": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer community
    "CSS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web technology
    "CSS Design Awards": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Design awards
    "CSS Modules": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web technology
    "CSS Wizardry": ["Professional, Scientific, and Technical Services", "Web Development"],  # Web consultancy
    "CSS3": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web technology
    "CTS": ["Transit and Ground Passenger Transportation", "Public Transportation"],  # Transit authority
    "Cucumber": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Cultura": ["Sporting Goods, Hobby, Musical Instrument, and Book Stores", "Retail Trade"],  # Retail chain
    "curl": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data transfer tool
    "CurseForge": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Mod platform
    "Custom Ink": ["Apparel Manufacturing", "Electronic Shopping and Mail-Order Houses"],  # Custom apparel
    "CyberDefenders": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Security training
    "Cycling '74": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Audio software
    "Cypress": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Cytoscape.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graph library
    "D": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "D-EDGE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Hotel technology
    "D-Wave Systems": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Quantum computing
    "D3": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data visualization
    "Dacia": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "DAF": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Truck manufacturer
    "daily.dev": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer news
    "Dailymotion": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Video platform
    "DaisyUI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Dapr": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Application runtime
    "Dark Reader": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Browser extension
    "Dart": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Darty": ["Electronics and Appliance Stores", "Retail Trade"],  # Electronics retailer
    "Das Erste": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # TV broadcaster
    "Dash": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "Dashlane": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Password manager
    "Dask": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data processing
    "Dassault Systèmes": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D software
    "data.ai": ["Professional, Scientific, and Technical Services", "Data Analytics"],  # Analytics platform
    "Databricks": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data platform
    "DataCamp": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Datadog": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring platform
    "DataGrip": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database IDE
    "Dataiku": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data science platform
    "DataStax": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database company
    "date-fns": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Date library
    "DATEV": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "DatoCMS": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Content platform
    "Datto": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IT solutions
    "DaVinci Resolve": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video editor
    "Dazhong Dianping": ["Data Processing, Hosting, and Related Services", "Internet Publishing and Broadcasting"],  # Review platform
    "DAZN": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # Sports streaming
    "DBeaver": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database tool
    "dblp": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Computer science bibliography
    "dbt": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data transformation
    "DC Entertainment": ["Motion Picture and Sound Recording Industries", "Publishing Industries (except Internet)"],  # Entertainment company
    "De'Longhi": ["Computer and Electronic Product Manufacturing", "Household Appliances"],  # Appliance manufacturer
    "Debian": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Debrid-Link": ["Data Processing, Hosting, and Related Services", "Internet Services"],  # Download service
    "Decap CMS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Content management
    "Decentraland": ["Software Publishers", "Entertainment"],  # Virtual world platform
    "DeepCool": ["Computer and Electronic Product Manufacturing", "Computer Equipment"],  # PC components
    "Deepgram": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Speech recognition
    "deepin": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "DeepL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Translation service
    "Deepnote": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data science platform
    "Deliveroo": ["Data Processing, Hosting, and Related Services", "Food Services and Drinking Places"],  # Food delivery
    "Dell": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Computer manufacturer
    "Delphi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Delta": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Deluge": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Torrent client
    "Deno": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript runtime
    "Denon": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "Dependabot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Dependency management
    "Depositphotos": ["Professional, Scientific, and Technical Services", "Stock Photography"],  # Stock photos
    "Der Spiegel": ["Internet Publishing and Broadcasting", "Other Information Services"],  # News publisher
    "Deutsche Bahn": ["Rail Transportation", "Transit and Ground Passenger Transportation"],  # Railway company
    "Deutsche Bank": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "Deutsche Post": ["Postal Service", "Couriers and Messengers"],  # Postal service
    "Deutsche Telekom": ["Telecommunications", "Internet Service Providers"],  # Telecom provider
    "Deutsche Welle": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # Broadcaster
    "dev.to": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer community
    "Devbox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "DevExpress": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "DeviantArt": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Art community
    "Devpost": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Hackathon platform
    "devRant": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Developer community
    "Dgraph": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "DHL": ["Postal Service", "Couriers and Messengers"],  # Logistics company
    "diagrams.net": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Diagramming tool
    "Dialogflow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chatbot platform
    "Diaspora": ["Software Publishers", "Social Networking Services"],  # Social network
    "Dictionary.com": ["Internet Publishing and Broadcasting", "Educational Services"],  # Online dictionary
    "Digg": ["Internet Publishing and Broadcasting", "Other Information Services"],  # News aggregator
    "Digi-Key Electronics": ["Electronic Shopping and Mail-Order Houses", "Electronics Manufacturing"],  # Electronics distributor
    "DigitalOcean": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "Diners Club": ["Credit Intermediation and Related Activities", "Financial Services"],  # Credit card company
    "Dior": ["Apparel Manufacturing", "Clothing and Clothing Accessories Stores"],  # Luxury fashion
    "Directus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Discogs": ["Electronic Shopping and Mail-Order Houses", "Internet Publishing and Broadcasting"],  # Music marketplace
    "Discord": ["Software Publishers", "Social Networking Services"],  # Communication platform
    "Discourse": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Forum software
    "Discover": ["Credit Intermediation and Related Activities", "Financial Services"],  # Financial services
    "Disqus": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Comment platform
    "Disroot": ["Data Processing, Hosting, and Related Services", "Internet Services"],  # Online services
    "Distrokid": ["Data Processing, Hosting, and Related Services", "Music Distribution"],  # Music distribution
    "Django": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "DJI": ["Computer and Electronic Product Manufacturing", "Drone Manufacturing"],  # Drone manufacturer
    "Dlib": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Machine learning library
    "DLNA": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Technology standard
    "dm": ["Health and Personal Care Stores", "Retail Trade"],  # Drugstore chain
    "Docker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container platform
    "Docs.rs": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Documentation hosting
    "Docsify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation tool
    "Doctrine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database toolkit
    "Docusaurus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation framework
    "Dogecoin": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency
    "DOI": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Digital identifier
    "Dolby": ["Computer and Electronic Product Manufacturing", "Audio Technology"],  # Audio technology
    "DoorDash": ["Data Processing, Hosting, and Related Services", "Food Services and Drinking Places"],  # Food delivery
    "Dota 2": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Video game
    "Douban": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "Douban Read": ["Internet Publishing and Broadcasting", "Electronic Shopping and Mail-Order Houses"],  # Book platform
    "Dovecot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email server
    "Dovetail": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Research platform
    "Downdetector": ["Data Processing, Hosting, and Related Services", "Internet Services"],  # Status monitoring
    "Doxygen": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation generator
    "DPD": ["Postal Service", "Couriers and Messengers"],  # Delivery service
    "Dragonframe": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Animation software
    "Draugiem.lv": ["Software Publishers", "Social Networking Services"],  # Social network
    "Dreamstime": ["Professional, Scientific, and Technical Services", "Stock Photography"],  # Stock photos
    "Dribbble": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Design community
    "Drizzle": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ORM tool
    "Drone": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI platform
    "Drooble": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Music community
    "Dropbox": ["Data Processing, Hosting, and Related Services", "Cloud Storage"],  # Cloud storage
    "Drupal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "DS Automobiles": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "DTS": ["Computer and Electronic Product Manufacturing", "Audio Technology"],  # Audio technology
    "DTube": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Video platform
    "Ducati": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Motorcycle manufacturer
    "DuckDB": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "DuckDuckGo": ["Data Processing, Hosting, and Related Services", "Internet Search Engines"],  # Search engine
    "Dungeons & Dragons": ["Publishing Industries (except Internet)", "Entertainment"],  # Game publisher
    "Dunked": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Portfolio platform
    "Dunzo": ["Data Processing, Hosting, and Related Services", "Couriers and Messengers"],  # Delivery service
    "Duolingo": ["Educational Services", "Software Publishers"],  # Language learning
    "Duplicati": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Backup software
    "DVC": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "dwm": ["Software Publishers", "Operating Systems"],  # Window manager
    "Dynatrace": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring platform
    "E.Leclerc": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "E3": ["Motion Picture and Sound Recording Industries", "Entertainment"],  # Gaming expo
    "EA": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game publisher
    "EAC": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Certification mark
    "Eagle": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Asset management
    "EasyEDA": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Circuit design
    "easyJet": ["Air Transportation", "Passenger Airlines"],  # Airline
    "eBay": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # Online marketplace
    "EBOX": ["Telecommunications", "Internet Service Providers"],  # Internet provider
    "Eclipse Adoptium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Java platform
    "Eclipse Che": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Eclipse IDE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development IDE
    "Eclipse Jetty": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web server
    "Eclipse Mosquitto": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # MQTT broker
    "Eclipse Vert.x": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Application framework
    "Ecosia": ["Data Processing, Hosting, and Related Services", "Internet Search Engines"],  # Search engine
    "Ecovacs": ["Computer and Electronic Product Manufacturing", "Household Appliances"],  # Robot manufacturer
    "EDEKA": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Edge Impulse": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML platform
    "EditorConfig": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code style tool
    "Educative": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "edX": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "egghead": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Egnyte": ["Data Processing, Hosting, and Related Services", "Cloud Storage"],  # File sharing
    "Eight": ["Professional, Scientific, and Technical Services", "Business Networking"],  # Business cards
    "Eight Sleep": ["Computer and Electronic Product Manufacturing", "Smart Home Technology"],  # Smart mattress
    "EJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Template engine
    "Elastic": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Search company
    "Elastic Cloud": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "Elastic Stack": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Software stack
    "Elasticsearch": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Search engine
    "Elavon": ["Credit Intermediation and Related Activities", "Financial Technology"],  # Payment processing
    "Electron": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Application framework
    "Electron Fiddle": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "electron-builder": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Elegoo": ["Computer and Electronic Product Manufacturing", "3D Printing"],  # 3D printer manufacturer
    "Element": ["Software Publishers", "Social Networking Services"],  # Chat platform
    "elementary": ["Software Publishers", "Operating Systems"],  # Operating system
    "Elementor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "ElevenLabs": ["Software Publishers", "Artificial Intelligence"],  # Voice AI
    "Eleventy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Static site generator
    "Elgato": ["Computer and Electronic Product Manufacturing", "Broadcasting Equipment"],  # Streaming equipment
    "Elixir": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Elm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Elsevier": ["Publishing Industries (except Internet)", "Professional, Scientific, and Technical Services"],  # Academic publisher
    "Embarcadero": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "Embark": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game studio
    "Ember.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Emby": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Media server
    "Emirates": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Emlakjet": ["Real Estate", "Data Processing, Hosting, and Related Services"],  # Real estate platform
    "Empire Kred": ["Software Publishers", "Social Networking Services"],  # Social platform
    "EndeavourOS": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Engadget": ["Internet Publishing and Broadcasting", "Other Information Services"],  # Tech news
    "Enpass": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Password manager
    "EnterpriseDB": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database company
    "Envato": ["Electronic Shopping and Mail-Order Houses", "Professional, Scientific, and Technical Services"],  # Digital marketplace
    "Envoy Proxy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Proxy software
    "EPEL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software repository
    "Epic Games": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game company
    "Epson": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "Equinix Metal": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "Eraser": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Diagramming tool
    "Ericsson": ["Computer and Electronic Product Manufacturing", "Telecommunications"],  # Telecom equipment
    "Erlang": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "ERPNext": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ERP software
    "esbuild": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "ESEA": ["Software Publishers", "Entertainment"],  # Gaming platform
    "ESLGaming": ["Motion Picture and Sound Recording Industries", "Entertainment"],  # Esports organization
    "ESLint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code linter
    "Esoteric Software": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game tools
    "ESPHome": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IoT framework
    "Espressif": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Chip manufacturer
    "ESRI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GIS software
    "etcd": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Key-value store
    "Ethereum": ["Financial Technology", "Blockchain Technology"],  # Cryptocurrency platform
    "Ethers": ["Software Publishers", "Blockchain Technology"],  # Blockchain library
    "Ethiopian Airlines": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Etihad Airways": ["Air Transportation", "Passenger Airlines"],  # Airline
    "Etsy": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # Online marketplace
    "European Union": ["Public Administration", "International Affairs"],  # Political union
    "Event Store": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Eventbrite": ["Data Processing, Hosting, and Related Services", "Entertainment"],  # Event platform
    "Evernote": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking platform
    "Excalidraw": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Drawing tool
    "Exercism": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Exordo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Conference management
    "Exoscale": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "Expedia": ["Data Processing, Hosting, and Related Services", "Travel Arrangement"],  # Travel platform
    "Expensify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Expense management
    "Experts Exchange": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Knowledge platform
    "Expo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Express": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Express.com": ["Clothing and Clothing Accessories Stores", "Electronic Shopping and Mail-Order Houses"],  # Fashion retailer
    "ExpressVPN": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # VPN service
    "EyeEm": ["Professional, Scientific, and Technical Services", "Stock Photography"],  # Photo platform
    "F-Droid": ["Software Publishers", "Electronic Shopping and Mail-Order Houses"],  # App store
    "F-Secure": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security software
    "F#": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "F1": ["Performing Arts, Spectator Sports, and Related Industries", "Entertainment"],  # Racing organization
    "F5": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Network software
    "Facebook": ["Data Processing, Hosting, and Related Services", "Social Networking Services"],  # Social network
    "Facebook Gaming": ["Software Publishers", "Entertainment"],  # Gaming platform
    "Facebook Live": ["Broadcasting (except Internet)", "Social Networking Services"],  # Streaming platform
    "FACEIT": ["Software Publishers", "Entertainment"],  # Gaming platform
    "Facepunch": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game developer
    "Fairphone": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Phone manufacturer
    "Falco": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security tool
    "Falcon": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "FamPay": ["Financial Technology", "Credit Intermediation and Related Activities"],  # Payment platform
    "Fandango": ["Data Processing, Hosting, and Related Services", "Motion Picture and Sound Recording Industries"],  # Movie ticketing
    "Fandom": ["Internet Publishing and Broadcasting", "Entertainment"],  # Wiki platform
    "Fanfou": ["Software Publishers", "Social Networking Services"],  # Social network
    "Fantom": ["Financial Technology", "Blockchain Technology"],  # Blockchain platform
    "Farcaster": ["Software Publishers", "Social Networking Services"],  # Social protocol
    "FareHarbor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Booking software
    "FARFETCH": ["Electronic Shopping and Mail-Order Houses", "Clothing and Clothing Accessories Stores"],  # Fashion platform
    "FastAPI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Fastify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Fastlane": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "Fastly": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # CDN provider
    "Fathom": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Fauna": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "Favro": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "FCC": ["Public Administration", "Telecommunications"],  # Government agency
    "FedEx": ["Couriers and Messengers", "Air Transportation"],  # Shipping company
    "Fedora": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Feedly": ["Software Publishers", "Internet Publishing and Broadcasting"],  # News aggregator
    "Ferrari": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Ferrari N.V.": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "FerretDB": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Database
    "FFmpeg": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Multimedia framework
    "Fi": ["Financial Technology", "Credit Intermediation and Related Activities"],  # Digital banking
    "Fiat": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Fido Alliance": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Authentication standard
    "FIFA": ["Performing Arts, Spectator Sports, and Related Industries", "Entertainment"],  # Sports organization
    "Fig": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Figma": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design platform
    "figshare": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Research platform
    "Fila": ["Apparel Manufacturing", "Sporting Goods, Hobby, Musical Instrument, and Book Stores"],  # Sportswear
    "Filament": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "File.io": ["Data Processing, Hosting, and Related Services", "Cloud Storage"],  # File sharing
    "Filen": ["Data Processing, Hosting, and Related Services", "Cloud Storage"],  # Cloud storage
    "Files": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # File management
    "FileZilla": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # FTP client
    "Fineco": ["Credit Intermediation and Related Activities", "Financial Services"],  # Banking
    "Fing": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Network tools
    "Firebase": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Development platform
    "Firefish": ["Software Publishers", "Social Networking Services"],  # Social platform
    "Firefly III": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Finance management
    "Firefox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "Firefox Browser": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "Fireship": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Firewalla": ["Computer and Electronic Product Manufacturing", "Network Security"],  # Network security
    "FIRST": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Robotics education
    "fish shell": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Shell
    "Fitbit": ["Computer and Electronic Product Manufacturing", "Wearable Technology"],  # Fitness devices
    "FiveM": ["Software Publishers", "Entertainment"],  # Game modification
    "Fiverr": ["Professional, Scientific, and Technical Services", "Electronic Shopping and Mail-Order Houses"],  # Freelance platform
    "Fizz": ["Telecommunications", "Internet Service Providers"],  # Mobile carrier
    "Flashforge": ["Computer and Electronic Product Manufacturing", "3D Printing"],  # 3D printer manufacturer
    "Flask": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Flat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Virtual classroom
    "Flathub": ["Software Publishers", "Electronic Shopping and Mail-Order Houses"],  # App store
    "Flatpak": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Flickr": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Photo platform
    "Flightaware": ["Data Processing, Hosting, and Related Services", "Air Transportation"],  # Flight tracking
    "Flipboard": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # News aggregator
    "Flipkart": ["Electronic Shopping and Mail-Order Houses", "Data Processing, Hosting, and Related Services"],  # E-commerce
    "Floatplane": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Video platform
    "Flood": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Load testing
    "Fluent Bit": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data collector
    "Fluentd": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Data collector
    "Fluke": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Test equipment
    "Flutter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development framework
    "Flux": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GitOps tool
    "Fly.io": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "Flyway": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database migration
    "FMOD": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Audio engine
    "Fnac": ["Electronics and Appliance Stores", "Retail Trade"],  # Retail chain
    "Folium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping library
    "Fonoma": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Font Awesome": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon library
    "FontBase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Font manager
    "FontForge": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Font editor
    "foobar2000": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Music player
    "foodpanda": ["Data Processing, Hosting, and Related Services", "Food Services and Drinking Places"],  # Food delivery
    "Ford": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Forgejo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git platform
    "Formik": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Form library
    "Formspree": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Form backend
    "Formstack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Form platform
    "Fortinet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security software
    "Fortran": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Fossa": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # License compliance
    "Fossil SCM": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "Foundry Virtual Tabletop": ["Software Publishers", "Entertainment"],  # Gaming platform
    "Foursquare": ["Data Processing, Hosting, and Related Services", "Social Networking Services"],  # Location platform
    "FOX": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # Broadcaster
    "Foxtel": ["Broadcasting (except Internet)", "Motion Picture and Sound Recording Industries"],  # TV provider
    "Fozzy": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Hosting provider
    "Framer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design tool
    "Framework": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Laptop manufacturer
    "Framework7": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mobile framework
    "Franprix": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Frappe": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Fraunhofer-Gesellschaft": ["Professional, Scientific, and Technical Services", "Research Organization"],  # Research organization
    "FreeBSD": ["Software Publishers", "Operating Systems"],  # Operating system
    "FreeCAD": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CAD software
    "freeCodeCamp": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "freedesktop.org": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Standards organization
    "Freelancer": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Freelance platform
    "freelancermap": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Freelance platform
    "FreeNAS": ["Software Publishers", "Data Processing, Hosting, and Related Services"],  # Storage software
    "freenet": ["Telecommunications", "Internet Service Providers"],  # Internet provider
    "Freepik": ["Professional, Scientific, and Technical Services", "Stock Photography"],  # Design resources
    "Fresh": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Frontend Mentor": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Frontify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Brand management
    "Fubo": ["Broadcasting (except Internet)", "Data Processing, Hosting, and Related Services"],  # Streaming service
    "Fueler": ["Professional, Scientific, and Technical Services", "Social Networking Services"],  # Portfolio platform
    "Fuga Cloud": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "Fujifilm": ["Computer and Electronic Product Manufacturing", "Photography Equipment"],  # Camera manufacturer
    "Fujitsu": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "Fur Affinity": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Art community
    "Furry Network": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Art community
    "FusionAuth": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Authentication platform
    "FutureLearn": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Fyle": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Expense management
    "G2": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Review platform
    "G2A": ["Electronic Shopping and Mail-Order Houses", "Entertainment"],  # Game marketplace
    "G2G": ["Electronic Shopping and Mail-Order Houses", "Entertainment"],  # Game marketplace
    "Galaxus": ["Electronic Shopping and Mail-Order Houses", "Retail Trade"],  # Online retailer
    "Game Developer": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Game news
    "Game Jolt": ["Electronic Shopping and Mail-Order Houses", "Entertainment"],  # Game platform
    "Game Science": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game developer
    "GameBanana": ["Internet Publishing and Broadcasting", "Entertainment"],  # Game mods
    "Gameloft": ["Software Publishers", "Motion Picture and Sound Recording Industries"],  # Game developer
    "Gamemaker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Garmin": ["Computer and Electronic Product Manufacturing", "Navigation Equipment"],  # GPS manufacturer
    "Gatling": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Load testing
    "Gatsby": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Gcore": ["Data Processing, Hosting, and Related Services", "Cloud Computing"],  # Cloud platform
    "GDAL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Geospatial library
    "GeeksforGeeks": ["Educational Services", "Internet Publishing and Broadcasting"],  # Learning platform
    "General Electric": ["Electrical Equipment Manufacturing", "Manufacturing"],  # Conglomerate
    "General Motors": ["Motor Vehicle Manufacturing", "Transportation Equipment Manufacturing"],  # Car manufacturer
    "Genius": ["Internet Publishing and Broadcasting", "Entertainment"],  # Lyrics platform
    "Gentoo": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Geocaching": ["Software Publishers", "Entertainment"],  # GPS game
    "Geode": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game modding
    "GeoPandas": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Geospatial library
    "Gerrit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code review
    "GetX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # App framework
    "Ghost": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Publishing platform
    "Ghostery": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Privacy tool
    "GIMP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image editor
    "Gin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "GIPHY": ["Internet Publishing and Broadcasting", "Entertainment"],  # GIF platform
    "Git": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "Git Extensions": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git client
    "Git for Windows": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "Git LFS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "GitBook": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation platform
    "Gitconnected": ["Professional, Scientific, and Technical Services", "Social Networking Services"],  # Developer network
    "Gitea": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git platform
    "Gitee": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git platform
    "GitHub": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "GitHub Actions": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "GitHub Copilot": ["Software Publishers", "Artificial Intelligence"],  # AI coding assistant
    "GitHub Pages": ["Data Processing, Hosting, and Related Services", "Internet Publishing and Broadcasting"],  # Web hosting
    "GitHub Sponsors": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Funding platform
    "gitignore.io": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "GitKraken": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git client
    "GitLab": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Gitpod": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "Gitter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat platform
    "GL.iNet": ["Computer and Electronic Product Manufacturing", "Telecommunications"],  # Router manufacturer
    "Glassdoor": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Job platform
    "Glide": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # App builder
    "Glitch": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Globus": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "Glovo": ["Data Processing, Hosting, and Related Services", "Food Services and Drinking Places"],  # Delivery service
    "glTF": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D format
    "Gmail": ["Data Processing, Hosting, and Related Services", "Internet Publishing and Broadcasting"],  # Email service
    "GMX": ["Data Processing, Hosting, and Related Services", "Internet Publishing and Broadcasting"],  # Email service
    "GNOME": ["Software Publishers", "Operating Systems"],  # Desktop environment
    "GNOME Terminal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal emulator
    "GNU": ["Software Publishers", "Operating Systems"],  # Operating system
    "GNU Bash": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Shell
    "GNU Emacs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "GNU IceCat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "GNU Privacy Guard": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Encryption software
    "GNU social": ["Software Publishers", "Social Networking Services"],  # Social network
    "Go": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "GoCD": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "GoDaddy": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "Godot Engine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "GoFundMe": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Crowdfunding platform
    "GOG.com": ["Software Publishers", "Entertainment"],  # Game distribution
    "Gojek": ["Transportation and Warehousing", "Food Services and Drinking Places"],  # Super app
    "GoLand": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "GoldenLine": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Job platform
    "Goldman Sachs": ["Securities, Commodity Contracts, and Other Financial Investments", "Banking"],  # Investment bank
    "Goodreads": ["Internet Publishing and Broadcasting", "Entertainment"],  # Book platform
    "Google": ["Software Publishers", "Internet Publishing and Broadcasting", "Advertising"],  # Tech giant
    "Google AdMob": ["Advertising", "Professional, Scientific, and Technical Services"],  # Mobile advertising
    "Google Ads": ["Advertising", "Professional, Scientific, and Technical Services"],  # Advertising platform
    "Google AdSense": ["Advertising", "Professional, Scientific, and Technical Services"],  # Advertising platform
    "Google Analytics": ["Professional, Scientific, and Technical Services", "Data Analytics"],  # Analytics platform
    "Google Apps Script": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Scripting platform
    "Google Assistant": ["Software Publishers", "Artificial Intelligence"],  # Virtual assistant
    "Google Authenticator": ["Software Publishers", "Information Security"],  # Security app
    "Google BigQuery": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Data warehouse
    "Google Bigtable": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Database
    "Google Calendar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Calendar service
    "Google Campaign Manager 360": ["Advertising", "Professional, Scientific, and Technical Services"],  # Ad management
    "Google Cardboard": ["Computer and Electronic Product Manufacturing", "Virtual Reality"],  # VR platform
    "Google Chat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat platform
    "Google Chrome": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "Google Chronicle": ["Software Publishers", "Information Security"],  # Security platform
    "Google Classroom": ["Software Publishers", "Educational Services"],  # Education platform
    "Google Cloud": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Google Cloud Composer": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Workflow platform
    "Google Cloud Spanner": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Database
    "Google Cloud Storage": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Storage service
    "Google Colab": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Google Container Optimized OS": ["Software Publishers", "Operating Systems"],  # Operating system
    "Google Data Studio": ["Software Publishers", "Data Analytics"],  # Analytics platform
    "Google Dataflow": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Data processing
    "Google Dataproc": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Data processing
    "Google Display & Video 360": ["Advertising", "Professional, Scientific, and Technical Services"],  # Ad platform
    "Google Docs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Document editor
    "Google Drive": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Storage service
    "Google Earth": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping service
    "Google Earth Engine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Geospatial platform
    "Google Fit": ["Software Publishers", "Health Care and Social Assistance"],  # Health platform
    "Google Fonts": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Font service
    "Google Forms": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Form service
    "Google Gemini": ["Software Publishers", "Artificial Intelligence"],  # AI model
    "Google Home": ["Computer and Electronic Product Manufacturing", "Smart Home"],  # Smart home
    "Google Keep": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Google Lens": ["Software Publishers", "Artificial Intelligence"],  # Visual AI
    "Google Maps": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping service
    "Google Marketing Platform": ["Advertising", "Professional, Scientific, and Technical Services"],  # Marketing platform
    "Google Meet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video conferencing
    "Google Messages": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Google Nearby": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Proximity service
    "Google News": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # News service
    "Google Pay": ["Software Publishers", "Banking"],  # Payment service
    "Google Photos": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Photo storage
    "Google Play": ["Software Publishers", "Retail Trade"],  # App store
    "Google Pub/Sub": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Messaging service
    "Google Scholar": ["Internet Publishing and Broadcasting", "Educational Services"],  # Academic search
    "Google Search Console": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # SEO tool
    "Google Sheets": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Spreadsheet app
    "Google Slides": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Presentation app
    "Google Street View": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Street imagery
    "Google Tag Manager": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics tool
    "Google Tasks": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Task management
    "Google Translate": ["Software Publishers", "Artificial Intelligence"],  # Translation service
    "GoToMeeting": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video conferencing
    "Grab": ["Transportation and Warehousing", "Food Services and Drinking Places"],  # Super app
    "Gradio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML UI library
    "Gradle": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Gradle Play Publisher": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Publishing tool
    "Grafana": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Grammarly": ["Software Publishers", "Artificial Intelligence"],  # Writing assistant
    "Grand Frais": ["Food and Beverage Stores", "Retail Trade"],  # Grocery chain
    "GrapheneOS": ["Software Publishers", "Operating Systems"],  # Mobile OS
    "Graphite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "GraphQL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Query language
    "Grav": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS
    "Gravatar": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Avatar service
    "Graylog": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Log management
    "Greasy Fork": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Script platform
    "Great Learning": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Education platform
    "Greenhouse": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Recruiting platform
    "GreenSock": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Animation library
    "Grid.ai": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML platform
    "Gridsome": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Grocy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ERP system
    "GroupMe": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Groupon": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Deal platform
    "Grubhub": ["Food Services and Drinking Places", "Transportation and Warehousing"],  # Food delivery
    "Grunt": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "GSK": ["Manufacturing", "Health Care and Social Assistance"],  # Pharmaceutical company
    "GSMArena.com": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Mobile news
    "GStreamer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Multimedia framework
    "GTK": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GUI toolkit
    "Guangzhou Metro": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Metro system
    "Guilded": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat platform
    "Guitar Pro": ["Software Publishers", "Entertainment"],  # Music software
    "gulp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build system
    "Gumroad": ["Internet Publishing and Broadcasting", "Retail Trade"],  # E-commerce platform
    "Gumtree": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Classifieds
    "Gunicorn": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web server
    "Gurobi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Optimization software
    "Gusto": ["Professional, Scientific, and Technical Services", "Administrative and Support Services"],  # HR platform
    "Gutenberg": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Editor
    "H&M": ["Retail Trade", "Clothing and Clothing Accessories Stores"],  # Fashion retail
    "H3": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Geospatial indexing
    "Habr": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech blog
    "Hack Club": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding education
    "Hack The Box": ["Educational Services", "Information Security"],  # Security training
    "Hackaday": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech blog
    "Hacker Noon": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech blog
    "HackerEarth": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Developer platform
    "HackerOne": ["Professional, Scientific, and Technical Services", "Information Security"],  # Security platform
    "HackerRank": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Developer platform
    "Hackster": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Hardware community
    "HAL": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Research archive
    "Handlebars.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Template engine
    "Handshake": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Career platform
    "HappyCow": ["Internet Publishing and Broadcasting", "Food Services and Drinking Places"],  # Restaurant guide
    "Harbor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Registry service
    "HarmonyOS": ["Software Publishers", "Operating Systems"],  # Mobile OS
    "HashiCorp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Infrastructure software
    "Hashnode": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Blog platform
    "Haskell": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Hasura": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GraphQL platform
    "Hatena Bookmark": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Social bookmarking
    "Have I Been Pwned": ["Professional, Scientific, and Technical Services", "Information Security"],  # Security service
    "Haxe": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "HBO": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Entertainment
    "HCL": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "HDFC Bank": ["Credit Intermediation and Related Activities", "Banking"],  # Banking
    "Headless UI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Headphone Zone": ["Retail Trade", "Electronics and Appliance Stores"],  # Audio retailer
    "Headspace": ["Health Care and Social Assistance", "Software Publishers"],  # Meditation app
    "Hearth": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Financial platform
    "hearthis.at": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music platform
    "Hedera": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain platform
    "Helium": ["Telecommunications", "Professional, Scientific, and Technical Services"],  # IoT network
    "Helix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "HelloFresh": ["Food Services and Drinking Places", "Retail Trade"],  # Meal kit service
    "Helly Hansen": ["Retail Trade", "Clothing and Clothing Accessories Stores"],  # Apparel manufacturer
    "Helm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Help Scout": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Customer service
    "HelpDesk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Support software
    "Hepsiemlak": ["Real Estate", "Professional, Scientific, and Technical Services"],  # Real estate platform
    "HERE": ["Professional, Scientific, and Technical Services", "Software Publishers"],  # Mapping platform
    "Hermes": ["Transportation and Warehousing", "Courier and Express Delivery Services"],  # Logistics
    "Heroku": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Hetzner": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Hosting provider
    "Hevy": ["Software Publishers", "Health Care and Social Assistance"],  # Fitness app
    "Hexlet": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Education platform
    "Hexo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blog framework
    "HEY": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email service
    "Hi Bob": ["Professional, Scientific, and Technical Services", "Administrative and Support Services"],  # HR platform
    "Hibernate": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ORM framework
    "Hilton": ["Accommodation and Food Services", "Hotels and Motels"],  # Hotel chain
    "Hilton Hotels & Resorts": ["Accommodation and Food Services", "Hotels and Motels"],  # Hotel chain
    "Hitachi": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Conglomerate
    "Hive": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Smart home
    "HiveMQ": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # MQTT platform
    "Homarr": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Dashboard
    "Home Assistant": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Home automation
    "Home Assistant Community Store": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Plugin store
    "HomeAdvisor": ["Professional, Scientific, and Technical Services", "Real Estate"],  # Home services
    "Homebrew": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Homebridge": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Home automation
    "Homepage": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Dashboard
    "homify": ["Professional, Scientific, and Technical Services", "Real Estate"],  # Home design
    "Honda": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Honey": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Shopping tool
    "Honeybadger": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Error tracking
    "Honeygain": ["Professional, Scientific, and Technical Services", "Internet Service Providers"],  # Network sharing
    "Hono": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Honor": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Mobile devices
    "Hootsuite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Social media
    "Hoppscotch": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API platform
    "Hostinger": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "Hotels.com": ["Accommodation and Food Services", "Travel Arrangement and Reservation Services"],  # Hotel booking
    "Hotjar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Hotwire": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Houdini": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D software
    "Houzz": ["Professional, Scientific, and Technical Services", "Real Estate"],  # Home design
    "HP": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Technology
    "HSBC": ["Credit Intermediation and Related Activities", "Banking"],  # Banking
    "HTC": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Mobile devices
    "HTC Vive": ["Computer and Electronic Product Manufacturing", "Virtual Reality"],  # VR hardware
    "HTML Academy": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding education
    "HTML5": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web standard
    "htmx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "htop": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # System monitor
    "HTTPie": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # HTTP client
    "Huawei": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Technology
    "HubSpot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Marketing platform
    "Hugging Face": ["Software Publishers", "Artificial Intelligence"],  # AI platform
    "Hugo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Static site generator
    "Humble Bundle": ["Software Publishers", "Retail Trade"],  # Game store
    "HumHub": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Social network
    "Hungry Jack's": ["Food Services and Drinking Places", "Limited-Service Restaurants"],  # Fast food
    "Husqvarna": ["Manufacturing", "Machinery Manufacturing"],  # Equipment manufacturer
    "Hyper": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal
    "Hyperskill": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "HyperX": ["Computer and Electronic Product Manufacturing", "Gaming Equipment"],  # Gaming peripherals
    "Hypothesis": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Annotation platform
    "Hyprland": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Window manager
    "Hyundai": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "i18next": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Localization framework
    "i3": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Window manager
    "Iata": ["Transportation and Warehousing", "Air Transportation"],  # Aviation organization
    "iBeacon": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Location tech
    "Iberia": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Iced": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GUI framework
    "Iceland": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket
    "ICICI Bank": ["Credit Intermediation and Related Activities", "Banking"],  # Banking
    "Icinga": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring
    "iCloud": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud storage
    "IcoMoon": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon tool
    "ICON": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain platform
    "Iconfinder": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Icon marketplace
    "Iconify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon framework
    "IconJar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon manager
    "Icons8": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Icon platform
    "ICQ": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging
    "IEEE": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Professional organization
    "iFixit": ["Professional, Scientific, and Technical Services", "Repair Services"],  # Repair guides
    "iFood": ["Food Services and Drinking Places", "Transportation and Warehousing"],  # Food delivery
    "IFTTT": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation platform
    "IGDB": ["Internet Publishing and Broadcasting", "Entertainment"],  # Game database
    "IGN": ["Internet Publishing and Broadcasting", "Entertainment"],  # Gaming media
    "iHeartRadio": ["Broadcasting", "Internet Publishing and Broadcasting"],  # Radio platform
    "IKEA": ["Furniture and Home Furnishings Stores", "Retail Trade"],  # Furniture retail
    "Île-de-France Mobilités": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit authority
    "Image.sc": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Scientific community
    "ImageJ": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image processing
    "IMDb": ["Internet Publishing and Broadcasting", "Entertainment"],  # Movie database
    "iMessage": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging
    "Imgur": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Image hosting
    "Immer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "Immich": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Photo management
    "Imou": ["Computer and Electronic Product Manufacturing", "Security Systems"],  # Security cameras
    "ImprovMX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email forwarding
    "Indeed": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Job platform
    "Indian Super League": ["Arts, Entertainment, and Recreation", "Spectator Sports"],  # Sports league
    "Indie Hackers": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Entrepreneur community
    "IndiGo": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Inductive Automation": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Industrial software
    "Inertia": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "INFINITI": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "InfluxDB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Time series database
    "Infomaniak": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "InfoQ": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech news
    "Informatica": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data integration
    "Infosys": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "Infracost": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud cost tool
    "Ingress": ["Software Publishers", "Entertainment"],  # AR game
    "Inkdrop": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Inkscape": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Vector graphics
    "Inoreader": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # RSS reader
    "Insomnia": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API client
    "INSPIRE": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Research platform
    "Insta360": ["Computer and Electronic Product Manufacturing", "Camera Equipment"],  # Camera manufacturer
    "Instacart": ["Retail Trade", "Food and Beverage Stores"],  # Grocery delivery
    "Instagram": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social media
    "Instapaper": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Reading platform
    "Instatus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Status page
    "Instructables": ["Internet Publishing and Broadcasting", "Educational Services"],  # DIY community
    "Instructure": ["Software Publishers", "Educational Services"],  # Education platform
    "Intel": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor
    "IntelliJ IDEA": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "Interaction Design Foundation": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Design education
    "InteractJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript library
    "Interbase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Intercom": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Customer messaging
    "Intermarche": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket
    "Internet Archive": ["Internet Publishing and Broadcasting", "Libraries and Archives"],  # Digital library
    "Internet Computer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain platform
    "Intigriti": ["Professional, Scientific, and Technical Services", "Information Security"],  # Bug bounty platform
    "Intuit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Financial software
    "InVision": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design platform
    "Invoice Ninja": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Invoicing software
    "ioBroker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Home automation
    "Ionic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mobile framework
    "Ionos": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "iOS": ["Software Publishers", "Operating Systems"],  # Mobile OS
    "IOTA": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain platform
    "IPFS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File system
    "IRIS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "iRobot": ["Computer and Electronic Product Manufacturing", "Robotics"],  # Robot manufacturer
    "ISC2": ["Professional, Scientific, and Technical Services", "Information Security"],  # Security organization
    "Issuu": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Publishing platform
    "Istio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Service mesh
    "Itch.io": ["Software Publishers", "Entertainment"],  # Game marketplace
    "iTerm2": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal emulator
    "iTunes": ["Software Publishers", "Entertainment"],  # Media player
    "ITVx": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV network
    "IVECO": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Vehicle manufacturer
    "Jabber": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging protocol
    "Jaeger": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring
    "Jaguar": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Jamboard": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Digital whiteboard
    "Jameson": ["Beverage Manufacturing", "Distilleries"],  # Whiskey brand
    "Jamstack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web architecture
    "Japan Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Jasmine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "JavaScript": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "JBL": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # Audio equipment
    "JCB": ["Credit Intermediation and Related Activities", "Credit Card Issuing"],  # Payment network
    "Jeep": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Jekyll": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Static site generator
    "Jellyfin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Media server
    "Jenkins": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Jest": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "JET": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "JetBlue": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "JetBrains": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "Jetpack Compose": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "JFrog": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # DevOps platform
    "JFrog Pipelines": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "JHipster": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Jinja": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Template engine
    "Jio": ["Telecommunications", "Wireless Telecommunications Carriers"],  # Telecom provider
    "Jira": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Jira Software": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "JitPack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package repository
    "Jitsi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video conferencing
    "John Deere": ["Machinery Manufacturing", "Agricultural Equipment Manufacturing"],  # Equipment manufacturer
    "Joomla": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Joplin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Jordan": ["Manufacturing", "Footwear Manufacturing"],  # Footwear brand
    "JOUAV": ["Computer and Electronic Product Manufacturing", "Aerospace Product Manufacturing"],  # Drone manufacturer
    "Jovian": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "JPEG": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image format
    "jQuery": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript library
    "JR Group": ["Transportation and Warehousing", "Rail Transportation"],  # Railway company
    "jsDelivr": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # CDN
    "JSFiddle": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code playground
    "JSON": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data format
    "JSON Web Tokens": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Authentication
    "JSR": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package registry
    "JSS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS in JS
    "JUCE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Audio framework
    "Juejin": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer community
    "JUKE": ["Retail Trade", "Electronics and Appliance Stores"],  # Electronics retailer
    "Julia": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Juniper Networks": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Network equipment
    "JUnit5": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Jupyter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Computing platform
    "Just Eat": ["Food Services and Drinking Places", "Transportation and Warehousing"],  # Food delivery
    "JustGiving": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Fundraising platform
    "K3s": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Kubernetes distribution
    "k6": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Load testing
    "Kaggle": ["Professional, Scientific, and Technical Services", "Data Analytics"],  # Data science platform
    "Kagi": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Search engine
    "Kahoot!": ["Software Publishers", "Educational Services"],  # Learning platform
    "KaiOS": ["Software Publishers", "Operating Systems"],  # Mobile OS
    "Kakao": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Internet company
    "KakaoTalk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Kali Linux": ["Software Publishers", "Information Security"],  # Security OS
    "Kamailio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # SIP server
    "Kaniko": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container tool
    "Karlsruher Verkehrsverbund": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit authority
    "Kasa Smart": ["Computer and Electronic Product Manufacturing", "Smart Home"],  # Smart home devices
    "KashFlow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Accounting software
    "Kaspersky": ["Software Publishers", "Information Security"],  # Security software
    "Katana": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D software
    "Kaufland": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "KDE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Desktop environment
    "KDE Plasma": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Desktop environment
    "Kdenlive": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video editor
    "Kedro": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data science framework
    "Keenetic": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Network equipment
    "Keep a Changelog": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation tool
    "KeePassXC": ["Software Publishers", "Information Security"],  # Password manager
    "Keeper": ["Software Publishers", "Information Security"],  # Password manager
    "KeeWeb": ["Software Publishers", "Information Security"],  # Password manager
    "Kentico": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Keras": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "Keybase": ["Software Publishers", "Information Security"],  # Security platform
    "KeyCDN": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # CDN
    "Keycloak": ["Software Publishers", "Information Security"],  # Identity management
    "Keystone": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS framework
    "KFC": ["Food Services and Drinking Places", "Limited-Service Restaurants"],  # Fast food
    "Khan Academy": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Education platform
    "Khronos Group": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Standards organization
    "Kia": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Kibana": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data visualization
    "KiCad": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # PCB design
    "Kick": ["Internet Publishing and Broadcasting", "Entertainment"],  # Streaming platform
    "Kickstarter": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Crowdfunding platform
    "Kik": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Kingston Technology": ["Computer and Electronic Product Manufacturing", "Computer Storage Manufacturing"],  # Hardware manufacturer
    "Kinopoisk": ["Internet Publishing and Broadcasting", "Entertainment"],  # Movie database
    "Kinsta": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "Kirby": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Kit": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Product platform
    "Kitsu": ["Internet Publishing and Broadcasting", "Entertainment"],  # Anime platform
    "Kiwix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Offline reader
    "Klarna": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment service
    "Kleinanzeigen": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Classifieds
    "KLM": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Klook": ["Travel Arrangement and Reservation Services", "Professional, Scientific, and Technical Services"],  # Travel platform
    "Knative": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Knex.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database tool
    "KNIME": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data analytics
    "Knip": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Dependency tool
    "KnowledgeBase": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Knowledge platform
    "Known": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Publishing platform
    "Ko-fi": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Donation platform
    "Koa": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Koc": ["Manufacturing", "Conglomerates"],  # Conglomerate
    "Kodak": ["Manufacturing", "Imaging Equipment"],  # Imaging company
    "Kodi": ["Software Publishers", "Entertainment"],  # Media player
    "Koenigsegg": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Kofax": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "Komoot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Navigation app
    "Konami": ["Software Publishers", "Entertainment"],  # Game company
    "Kong": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API platform
    "Kongregate": ["Internet Publishing and Broadcasting", "Entertainment"],  # Game platform
    "Konva": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics library
    "Kotlin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Koyeb": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Krita": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Digital art
    "KTM": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Motorcycle manufacturer
    "Ktor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Kuaishou": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Video platform
    "Kubernetes": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container platform
    "Kubuntu": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "KuCoin": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Crypto exchange
    "Kueski": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Fintech
    "Kuma": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Service mesh
    "Kununu": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Employer reviews
    "Kuula": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # VR platform
    "KX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data platform
    "Kyocera": ["Computer and Electronic Product Manufacturing", "Office Equipment Manufacturing"],  # Electronics manufacturer
    "L'Équipe": ["Internet Publishing and Broadcasting", "Sports Media"],  # Sports media
    "LabVIEW": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Engineering software
    "LADA": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Lamborghini": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Land Rover": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "LangChain": ["Software Publishers", "Artificial Intelligence"],  # AI framework
    "Langflow": ["Software Publishers", "Artificial Intelligence"],  # AI platform
    "LangGraph": ["Software Publishers", "Artificial Intelligence"],  # AI framework
    "LanguageTool": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Writing tool
    "Lapce": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "Laragon": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "Laravel": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Laravel Horizon": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Queue monitor
    "Laravel Nova": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Admin panel
    "Last.fm": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music platform
    "LastPass": ["Software Publishers", "Information Security"],  # Password manager
    "LaTeX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Document preparation
    "Launchpad": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Lazarus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "LazyVim": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "LBRY": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Content platform
    "Leader Price": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Leaflet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping library
    "League of Legends": ["Software Publishers", "Entertainment"],  # Video game
    "Leanpub": ["Internet Publishing and Broadcasting", "Publishing Industries"],  # Publishing platform
    "LeetCode": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding platform
    "Lefthook": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git hooks
    "Legacy Games": ["Software Publishers", "Entertainment"],  # Game publisher
    "Leica": ["Computer and Electronic Product Manufacturing", "Camera Equipment"],  # Camera manufacturer
    "Lemmy": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social platform
    "Lemon Squeezy": ["Professional, Scientific, and Technical Services", "E-commerce"],  # Payment platform
    "Lenovo": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Hardware manufacturer
    "Lens": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Kubernetes IDE
    "Leptos": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Lerna": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Leroy Merlin": ["Building Material and Garden Equipment and Supplies Dealers", "Retail Trade"],  # Home improvement
    "Les libraires": ["Book Stores", "Retail Trade"],  # Bookstore
    "Less": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS preprocessor
    "Let's Encrypt": ["Professional, Scientific, and Technical Services", "Information Security"],  # Certificate authority
    "Letterboxd": ["Internet Publishing and Broadcasting", "Entertainment"],  # Film platform
    "levels.fyi": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Salary platform
    "LG": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "Li-Ning": ["Clothing and Clothing Accessories Stores", "Retail Trade"],  # Sportswear
    "Libera.Chat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat network
    "Liberapay": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Donation platform
    "Libraries.io": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Package registry
    "LibraryThing": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Book platform
    "LibreOffice": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Office suite
    "LibreOffice Base": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database software
    "LibreOffice Calc": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Spreadsheet software
    "LibreOffice Draw": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Drawing software
    "LibreOffice Impress": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Presentation software
    "LibreOffice Math": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Math software
    "LibreOffice Writer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Word processor
    "LibreTranslate": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Translation software
    "LibreTube": ["Software Publishers", "Entertainment"],  # Video platform
    "LibreWolf": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "libuv": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software library
    "Lichess": ["Internet Publishing and Broadcasting", "Entertainment"],  # Chess platform
    "Lidl": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "LIFX": ["Computer and Electronic Product Manufacturing", "Smart Home"],  # Smart lighting
    "LightBurn": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Laser software
    "Lighthouse": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web tool
    "Lightning": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "LimeSurvey": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Survey platform
    "LINE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "LineageOS": ["Software Publishers", "Operating Systems"],  # Mobile OS
    "Linear": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Linkerd": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Service mesh
    "Linkfire": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Marketing platform
    "Linksys": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Network equipment
    "Linktree": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Link platform
    "Linphone": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # VoIP software
    "LintCode": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Coding platform
    "Linux": ["Software Publishers", "Operating Systems"],  # Operating system
    "Linux Containers": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container platform
    "Linux Foundation": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Tech foundation
    "Linux Mint": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Linux Professional Institute": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Certification org
    "LinuxServer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container platform
    "Lion Air": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Liquibase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database tool
    "listmonk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email platform
    "Lit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web components
    "Litecoin": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Cryptocurrency
    "Literal": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Reading platform
    "LITIENGINE": ["Software Publishers", "Entertainment"],  # Game engine
    "LiveChat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Customer service
    "LiveJournal": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Blogging platform
    "Livewire": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "LLVM": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Compiler infrastructure
    "LMMS": ["Software Publishers", "Entertainment"],  # Music software
    "Lobsters": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech community
    "Local": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "Lodash": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript library
    "Logitech": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Hardware manufacturer
    "Logitech G": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Gaming hardware
    "LogMeIn": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Remote access
    "Logseq": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Logstash": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Log management
    "Looker": ["Software Publishers", "Data Analytics"],  # Business intelligence
    "Loom": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video messaging
    "Loop": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Research platform
    "LoopBack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API framework
    "Loot Crate": ["Retail Trade", "Miscellaneous Store Retailers"],  # Subscription box
    "Lospec": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Art platform
    "LOT Polish Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "LottieFiles": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Animation platform
    "LTspice": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Circuit simulation
    "Lua": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Lubuntu": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Lucia": ["Software Publishers", "Information Security"],  # Authentication
    "Lucid": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Collaboration software
    "Lucide": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon library
    "Ludwig": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "Lufthansa": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Lumen": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Lunacy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design tool
    "Lutris": ["Software Publishers", "Entertainment"],  # Game platform
    "LVGL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics library
    "Lydia": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment app
    "Lyft": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Ride-sharing
    "MAAS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Infrastructure software
    "macOS": ["Software Publishers", "Operating Systems"],  # Operating system
    "MacPaw": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software developer
    "Macy's": ["General Merchandise Stores", "Retail Trade"],  # Department store
    "Magasins U": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Magic": ["Software Publishers", "Information Security"],  # Authentication platform
    "Magisk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Android customization
    "Mahindra": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "mail.com": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Email service
    "Mail.Ru": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Internet company
    "mailbox.org": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Email service
    "MailChimp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email marketing
    "Mailgun": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email service
    "Mailtrap": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email testing
    "MainWP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # WordPress management
    "Major League Hacking": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Tech education
    "Make": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation platform
    "MakerBot": ["Computer and Electronic Product Manufacturing", "Manufacturing"],  # 3D printing
    "Malt": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Freelance platform
    "Malwarebytes": ["Software Publishers", "Information Security"],  # Security software
    "Mamba UI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "MAMP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "MAN": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Vehicle manufacturer
    "ManageIQ": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud management
    "Manjaro": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Mantine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Mapbox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping platform
    "Mapillary": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Street-level imagery
    "MapLibre": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping library
    "MapTiler": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping platform
    "MariaDB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "MariaDB Foundation": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Database organization
    "Markdown": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Markup language
    "Marko": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Marriott": ["Accommodation", "Hotels and Motels"],  # Hotel chain
    "MarvelApp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design platform
    "Maserati": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "MasterCard": ["Credit Intermediation and Related Activities", "Credit Card Issuing"],  # Payment network
    "mastercomfig": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game configuration
    "Mastodon": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "Material Design": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design system
    "Material Design Icons": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon library
    "Material for MkDocs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation tool
    "Matillion": ["Software Publishers", "Data Analytics"],  # Data integration
    "Matomo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Matrix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Communication protocol
    "Matter.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Physics engine
    "Mattermost": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Team chat
    "Matternet": ["Transportation Equipment Manufacturing", "Aerospace Product Manufacturing"],  # Drone delivery
    "Mautic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Marketing automation
    "Max": ["Software Publishers", "Entertainment"],  # Audio software
    "Max-Planck-Gesellschaft": ["Professional, Scientific, and Technical Services", "Research Organizations"],  # Research organization
    "Maytag": ["Computer and Electronic Product Manufacturing", "Appliance Manufacturing"],  # Appliance manufacturer
    "Mazda": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Maze": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design platform
    "McAfee": ["Software Publishers", "Information Security"],  # Security software
    "McDonald's": ["Food Services and Drinking Places", "Limited-Service Restaurants"],  # Fast food
    "McLaren": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "mdBook": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation tool
    "MDN Web Docs": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer docs
    "MDX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation format
    "Mealie": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Recipe manager
    "MediaFire": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # File hosting
    "MediaMarkt": ["Electronics and Appliance Stores", "Retail Trade"],  # Electronics retailer
    "MediaPipe": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "MediaTek": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor manufacturer
    "MediBang Paint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Digital art
    "Medium": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Publishing platform
    "Medusa": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # E-commerce platform
    "Meetup": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Event platform
    "MEGA": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud storage
    "Meilisearch": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Search engine
    "Meituan": ["Food Services and Drinking Places", "Transportation and Warehousing"],  # Delivery platform
    "Meizu": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Mobile devices
    "Mendeley": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Research platform
    "MentorCruise": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Mentorship platform
    "Mercado Pago": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment service
    "Mercedes": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Merck": ["Chemical Manufacturing", "Pharmaceutical Manufacturing"],  # Pharmaceutical company
    "Mercurial": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "Mermaid": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Diagramming tool
    "Messenger": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Meta": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Technology company
    "Metabase": ["Software Publishers", "Data Analytics"],  # Business intelligence
    "Metacritic": ["Internet Publishing and Broadcasting", "Entertainment"],  # Review aggregator
    "MetaFilter": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Community platform
    "Metasploit": ["Software Publishers", "Information Security"],  # Security tool
    "Meteor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Metro": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Metro de la Ciudad de México": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "Metro de Madrid": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "Métro de Paris": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "MeWe": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "MG": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Micro Editor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "micro:bit": ["Computer and Electronic Product Manufacturing", "Educational Services"],  # Educational hardware
    "Micro.blog": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Blogging platform
    "MicroPython": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Microstation": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CAD software
    "MicroStrategy": ["Software Publishers", "Data Analytics"],  # Business intelligence
    "MIDI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Music standard
    "Migadu": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Email service
    "miHoYo": ["Software Publishers", "Entertainment"],  # Game developer
    "MikroTik": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Network equipment
    "Milanote": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Milvus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Vector database
    "Minds": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "Minetest": ["Software Publishers", "Entertainment"],  # Game engine
    "MinGW-w64": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "Mini": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "MinIO": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Storage platform
    "Mintlify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation platform
    "Minutemailer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email platform
    "Miraheze": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Wiki hosting
    "Miro": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Collaboration platform
    "Misskey": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social platform
    "Mitsubishi": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Conglomerate
    "Mix": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Content discovery
    "Mixcloud": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music platform
    "Mixpanel": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "MLB": ["Arts, Entertainment, and Recreation", "Spectator Sports"],  # Sports league
    "MLflow": ["Software Publishers", "Artificial Intelligence"],  # ML platform
    "MobX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "MobX-State-Tree": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "Mocha": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Mock Service Worker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API mocking
    "Modal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Modin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data framework
    "Modrinth": ["Internet Publishing and Broadcasting", "Entertainment"],  # Game mods
    "MODX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Mojeek": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Search engine
    "Moleculer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Microservices
    "Momenteo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "Monero": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Cryptocurrency
    "MoneyGram": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Money transfer
    "MongoDB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Mongoose": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database tool
    "Monica": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CRM
    "monkey tie": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Recruitment platform
    "Monkeytype": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Typing platform
    "MonoGame": ["Software Publishers", "Entertainment"],  # Game framework
    "Monoprix": ["Food and Beverage Stores", "Retail Trade"],  # Retail chain
    "Monster": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Job platform
    "Monzo": ["Credit Intermediation and Related Activities", "Banking"],  # Digital bank
    "Moo": ["Printing and Related Support Activities", "Professional, Scientific, and Technical Services"],  # Print services
    "Moodle": ["Software Publishers", "Educational Services"],  # Learning platform
    "Moonrepo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Moq": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Moqups": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design platform
    "Morrisons": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Moscow Metro": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "Motorola": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Electronics manufacturer
    "Movistar": ["Telecommunications", "Wireless Telecommunications Carriers"],  # Telecom provider
    "Mozilla": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Technology organization
    "mpv": ["Software Publishers", "Entertainment"],  # Media player
    "MQTT": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Protocol
    "MSI": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Hardware manufacturer
    "MSI Business": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Business hardware
    "MTA": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit authority
    "MTR": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "MUBI": ["Internet Publishing and Broadcasting", "Entertainment"],  # Streaming service
    "MUI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Mulesoft": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Integration platform
    "Müller": ["Health and Personal Care Stores", "Retail Trade"],  # Retail chain
    "Mullvad": ["Software Publishers", "Information Security"],  # VPN service
    "Multisim": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Circuit simulation
    "Mumble": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Voice chat
    "MUO": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech publication
    "Mural": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Collaboration platform
    "MuseScore": ["Software Publishers", "Entertainment"],  # Music software
    "MusicBrainz": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music database
    "MX Linux": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "MyAnimeList": ["Internet Publishing and Broadcasting", "Entertainment"],  # Anime database
    "MyGet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package hosting
    "MYOB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Accounting software
    "Myspace": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "MySQL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "N26": ["Credit Intermediation and Related Activities", "Banking"],  # Digital bank
    "n8n": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation platform
    "Namebase": ["Professional, Scientific, and Technical Services", "Domain Services"],  # Domain registrar
    "Namecheap": ["Professional, Scientific, and Technical Services", "Domain Services"],  # Domain registrar
    "NameMC": ["Internet Publishing and Broadcasting", "Entertainment"],  # Minecraft names
    "NameSilo": ["Professional, Scientific, and Technical Services", "Domain Services"],  # Domain registrar
    "Namu Wiki": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Wiki platform
    "Nano": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Cryptocurrency
    "Nano Stores": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "Napster": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music service
    "NASA": ["Professional, Scientific, and Technical Services", "Research Organizations"],  # Space agency
    "National Grid": ["Utilities", "Electric Power Generation"],  # Utility company
    "National Rail": ["Transportation and Warehousing", "Rail Transportation"],  # Rail system
    "NativeScript": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mobile framework
    "NATS.io": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging system
    "Naver": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Internet company
    "NBA": ["Arts, Entertainment, and Recreation", "Spectator Sports"],  # Sports league
    "NBB": ["Electronics and Appliance Stores", "Retail Trade"],  # Electronics retailer
    "NBC": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV network
    "NDR": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Broadcasting company
    "NEAR": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain platform
    "Nebula": ["Internet Publishing and Broadcasting", "Entertainment"],  # Streaming service
    "NEC": ["Computer and Electronic Product Manufacturing", "Professional, Scientific, and Technical Services"],  # Technology company
    "Neo4j": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Neovim": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "Neptune": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML platform
    "NestJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "NetApp": ["Computer and Electronic Product Manufacturing", "Data Storage"],  # Storage solutions
    "NetBSD": ["Software Publishers", "Operating Systems"],  # Operating system
    "netcup": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "Netdata": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring
    "NetEase Cloud Music": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music platform
    "Netflix": ["Internet Publishing and Broadcasting", "Entertainment"],  # Streaming service
    "NETGEAR": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Network equipment
    "Netlify": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "Nette": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Netto": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Neutralinojs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Desktop framework
    "New Balance": ["Manufacturing", "Footwear Manufacturing"],  # Footwear manufacturer
    "New Japan Pro-Wrestling": ["Arts, Entertainment, and Recreation", "Spectator Sports"],  # Wrestling promotion
    "New Relic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring platform
    "New York Times": ["Internet Publishing and Broadcasting", "Publishing Industries"],  # News organization
    "Newegg": ["Electronics and Appliance Stores", "Retail Trade"],  # Electronics retailer
    "NEXON": ["Software Publishers", "Entertainment"],  # Game company
    "Next.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "NextBillion.ai": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping platform
    "Nextcloud": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "NextDNS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # DNS service
    "Nextdoor": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "Nextflow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Workflow platform
    "Nextra": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation framework
    "NextUI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Nexus Mods": ["Internet Publishing and Broadcasting", "Entertainment"],  # Game mods
    "nf-core": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Pipeline framework
    "NFC": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Technology standard
    "NGINX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web server
    "Nginx Proxy Manager": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Proxy manager
    "ngrok": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Tunneling service
    "NgRx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "NHL": ["Arts, Entertainment, and Recreation", "Spectator Sports"],  # Sports league
    "NiceHash": ["Software Publishers", "Digital Assets"],  # Mining platform
    "niconico": ["Internet Publishing and Broadcasting", "Entertainment"],  # Video platform
    "Nike": ["Manufacturing", "Footwear Manufacturing"],  # Sportswear manufacturer
    "Nikon": ["Computer and Electronic Product Manufacturing", "Camera Equipment"],  # Camera manufacturer
    "Nim": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Nissan": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "NixOS": ["Software Publishers", "Operating Systems"],  # Operating system
    "Node-RED": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Flow programming
    "Node.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Runtime environment
    "Nodemon": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Nokia": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Technology company
    "Nomad": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Orchestration platform
    "Norco": ["Transportation Equipment Manufacturing", "Bicycle Manufacturing"],  # Bicycle manufacturer
    "Nordic Semiconductor": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor company
    "NordVPN": ["Software Publishers", "Information Security"],  # VPN service
    "Normalize.css": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS framework
    "Norton": ["Software Publishers", "Information Security"],  # Security software
    "Norwegian": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Notepad++": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "Notion": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Productivity platform
    "Notist": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Presentation platform
    "Noun Project": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Icon platform
    "Novu": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Notification platform
    "NOW": ["Internet Publishing and Broadcasting", "Entertainment"],  # Streaming service
    "npm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Nrwl": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "NSIS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Installer system
    "ntfy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Notification service
    "Nubank": ["Credit Intermediation and Related Activities", "Banking"],  # Digital bank
    "Nucleo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon management
    "NuGet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Nuke": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Visual effects
    "Numba": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Python compiler
    "NumPy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Scientific computing
    "Nunjucks": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Template engine
    "Nushell": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Shell
    "Nutanix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud computing
    "Nuxt": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "NVIDIA": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Technology company
    "nvm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version manager
    "Nx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "NXP": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor company
    "NZXT": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Hardware manufacturer
    "O'Reilly": ["Internet Publishing and Broadcasting", "Publishing Industries"],  # Technical publisher
    "O2": ["Telecommunications", "Wireless Telecommunications Carriers"],  # Telecom provider
    "ÖBB": ["Transportation and Warehousing", "Rail Transportation"],  # Railway company
    "OBS Studio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Streaming software
    "Observable": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data visualization
    "Obsidian": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Obtainium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # App updates
    "OCaml": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "OCLC": ["Professional, Scientific, and Technical Services", "Libraries and Archives"],  # Library organization
    "oclif": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CLI framework
    "Octane Render": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D rendering
    "Octave": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Scientific computing
    "October CMS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "OctoPrint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D printing control
    "Octopus Deploy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Deployment platform
    "Oculus": ["Computer and Electronic Product Manufacturing", "Virtual Reality"],  # VR hardware
    "Odin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Odnoklassniki": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "Odoo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "Odysee": ["Internet Publishing and Broadcasting", "Entertainment"],  # Video platform
    "Oh Dear": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website monitoring
    "okcupid": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Dating platform
    "Okta": ["Software Publishers", "Information Security"],  # Identity management
    "OKX": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Crypto exchange
    "Ollama": ["Software Publishers", "Artificial Intelligence"],  # AI platform
    "Omada Cloud": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Network management
    "OnePlus": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Mobile devices
    "OnlyFans": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Content platform
    "ONLYOFFICE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Office suite
    "ONNX": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "OnStar": ["Professional, Scientific, and Technical Services", "Telematics"],  # Vehicle services
    "Opel": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Open Access": ["Professional, Scientific, and Technical Services", "Research Organizations"],  # Research initiative
    "Open Badges": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Digital credentials
    "Open Bug Bounty": ["Professional, Scientific, and Technical Services", "Information Security"],  # Security platform
    "Open Collective": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Funding platform
    "Open Containers Initiative": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Standards organization
    "Open Source Hardware": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Standards organization
    "Open Source Initiative": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Standards organization
    "Open3D": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D processing
    "OpenAI": ["Software Publishers", "Artificial Intelligence"],  # AI company
    "OpenAI Gym": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "OpenAPI Initiative": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Standards organization
    "OpenBSD": ["Software Publishers", "Operating Systems"],  # Operating system
    "OpenCV": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Computer vision
    "OpenFaaS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Serverless platform
    "OpenGL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics API
    "openHAB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Home automation
    "OpenID": ["Software Publishers", "Information Security"],  # Authentication protocol
    "OpenJDK": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "OpenJS Foundation": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Standards organization
    "Openlayers": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mapping library
    "openmediavault": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Storage platform
    "OpenMined": ["Software Publishers", "Artificial Intelligence"],  # Privacy platform
    "OpenNebula": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "OpenProject": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "OpenSCAD": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CAD software
    "OpenSea": ["Internet Publishing and Broadcasting", "Digital Assets"],  # NFT marketplace
    "OpenSearch": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Search engine
    "OpenSSL": ["Software Publishers", "Information Security"],  # Security library
    "OpenStack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "OpenStreetMap": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Mapping platform
    "openSUSE": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "OpenTelemetry": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Observability framework
    "OpenText": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Enterprise software
    "OpenTofu": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Infrastructure tool
    "Openverse": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Media search
    "OpenVPN": ["Software Publishers", "Information Security"],  # VPN software
    "OpenWrt": ["Software Publishers", "Operating Systems"],  # Router software
    "OpenZeppelin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain security
    "OpenZFS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File system
    "Opera": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "Opera GX": ["Software Publishers", "Entertainment"],  # Gaming browser
    "OPNSense": ["Software Publishers", "Information Security"],  # Firewall software
    "OPPO": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Mobile devices
    "Opsgenie": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Incident management
    "OpsLevel": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Service catalog
    "Optimism": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain platform
    "Orange": ["Telecommunications", "Wireless Telecommunications Carriers"],  # Telecom provider
    "ORCID": ["Professional, Scientific, and Technical Services", "Research Organizations"],  # Research ID system
    "Org": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Document format
    "Organic Maps": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Navigation app
    "Origin": ["Software Publishers", "Entertainment"],  # Game platform
    "Osano": ["Software Publishers", "Information Security"],  # Privacy platform
    "OSF": ["Professional, Scientific, and Technical Services", "Research Organizations"],  # Research platform
    "OSGeo": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Geospatial organization
    "Oshkosh": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Vehicle manufacturer
    "OSMC": ["Software Publishers", "Entertainment"],  # Media center
    "osu!": ["Software Publishers", "Entertainment"],  # Rhythm game
    "Otto": ["Retail Trade", "Nonstore Retailers"],  # E-commerce
    "Outline": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation platform
    "Overcast": ["Software Publishers", "Entertainment"],  # Podcast player
    "Overleaf": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Document editor
    "OVH": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud provider
    "OWASP": ["Professional, Scientific, and Technical Services", "Information Security"],  # Security organization
    "OWASP Dependency-Check": ["Software Publishers", "Information Security"],  # Security tool
    "ownCloud": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File sharing
    "Oxygen": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "OYO": ["Accommodation", "Hotels and Motels"],  # Hotel chain
    "p5.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics library
    "Packagist": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package repository
    "Packer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image builder
    "Packt": ["Internet Publishing and Broadcasting", "Publishing Industries"],  # Technical publisher
    "Paddle": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "PaddlePaddle": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "Paddy Power": ["Amusement, Gambling, and Recreation Industries", "Gambling Industries"],  # Betting company
    "Pagekit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "PagerDuty": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Incident management
    "PageSpeed Insights": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Performance tool
    "PagSeguro": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "Palantir": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data platform
    "Palo Alto Networks": ["Software Publishers", "Information Security"],  # Security company
    "Palo Alto Software": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "Panasonic": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "pandas": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data analysis
    "Pandora": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music service
    "Pantheon": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "Paperless-ngx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Document management
    "Papers With Code": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Research platform
    "Paperspace": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Paradox Interactive": ["Software Publishers", "Entertainment"],  # Game publisher
    "Paramount+": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Streaming service
    "Parity Substrate": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain framework
    "Parrot Security": ["Software Publishers", "Information Security"],  # Security OS
    "Parse.ly": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Passport": ["Software Publishers", "Information Security"],  # Authentication library
    "Pastebin": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Text sharing
    "Patreon": ["Professional, Scientific, and Technical Services", "Crowdfunding"],  # Funding platform
    "Paychex": ["Professional, Scientific, and Technical Services", "Administrative and Support Services"],  # HR services
    "Payhip": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # E-commerce platform
    "Payload CMS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Payoneer": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "PayPal": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "Paytm": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "PCGamingWiki": ["Internet Publishing and Broadcasting", "Entertainment"],  # Gaming wiki
    "PDM": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "PDQ": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IT management
    "Peak Design": ["Manufacturing", "Camera Equipment"],  # Camera accessories
    "Pearson": ["Educational Services", "Publishing Industries"],  # Education company
    "Peerlist": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Professional network
    "PeerTube": ["Internet Publishing and Broadcasting", "Entertainment"],  # Video platform
    "Pegasus Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Pelican": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Static site generator
    "Peloton": ["Manufacturing", "Sporting Goods Manufacturing"],  # Fitness equipment
    "Penny": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Penpot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design platform
    "Percy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Visual testing
    "Perforce": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "Perl": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Perplexity": ["Software Publishers", "Artificial Intelligence"],  # AI search
    "Persistent": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "Personio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # HR software
    "Pets at Home": ["Retail Trade", "Pet Supplies"],  # Pet retailer
    "Peugeot": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Pexels": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Stock photos
    "pfSense": ["Software Publishers", "Information Security"],  # Firewall software
    "Phabricator": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Philips Hue": ["Computer and Electronic Product Manufacturing", "Smart Home"],  # Smart lighting
    "Phoenix Framework": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "PhonePe": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "Phosphor Icons": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon library
    "Photobucket": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Image hosting
    "Photocrowd": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Photography platform
    "Photon": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game networking
    "Photopea": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image editor
    "PHP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "phpBB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Forum software
    "phpMyAdmin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database tool
    "PhpStorm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "Pi Network": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Cryptocurrency
    "Pi-hole": ["Software Publishers", "Information Security"],  # Network tool
    "Piaggio Group": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Vehicle manufacturer
    "Piapro": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music platform
    "Picard Surgelés": ["Food and Beverage Stores", "Retail Trade"],  # Frozen food retailer
    "Picarto.TV": ["Internet Publishing and Broadcasting", "Entertainment"],  # Streaming platform
    "Picnic": ["Food and Beverage Stores", "Retail Trade"],  # Online grocery
    "PicPay": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "Picrew": ["Internet Publishing and Broadcasting", "Entertainment"],  # Avatar creator
    "Picsart": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Photo editor
    "Picxy": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Stock photos
    "Pimcore": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Digital platform
    "Pinboard": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Bookmarking service
    "Pine Script": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Trading language
    "Pingdom": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring service
    "pino": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Logging library
    "Pinterest": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social platform
    "Pioneer DJ": ["Computer and Electronic Product Manufacturing", "Audio Equipment"],  # DJ equipment
    "Piped": ["Internet Publishing and Broadcasting", "Entertainment"],  # Video platform
    "pipx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package installer
    "Pivotal Tracker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Piwigo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Photo gallery
    "Pix": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment system
    "Pixabay": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Stock photos
    "Pixelfed": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Photo sharing
    "pixiv": ["Internet Publishing and Broadcasting", "Entertainment"],  # Art platform
    "Pixlr": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Photo editor
    "pkgsrc": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Planet": ["Professional, Scientific, and Technical Services", "Satellite Imaging"],  # Satellite imaging
    "PlanetScale": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database platform
    "PlanGrid": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Construction software
    "Platform.sh": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "PlatformIO": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Platzi": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Plausible Analytics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "PlayCanvas": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game engine
    "Player FM": ["Internet Publishing and Broadcasting", "Entertainment"],  # Podcast platform
    "Player.me": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Gaming community
    "PlayStation": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Gaming platform
    "PlayStation 2": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Gaming console
    "PlayStation 3": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Gaming console
    "PlayStation 4": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Gaming console
    "PlayStation 5": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Gaming console
    "PlayStation Portable": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Gaming console
    "PlayStation Vita": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Gaming console
    "Pleroma": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social platform
    "Plesk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Server management
    "Plex": ["Software Publishers", "Entertainment"],  # Media server
    "Plotly": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data visualization
    "Plume": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # WiFi systems
    "Pluralsight": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Plurk": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social platform
    "Plus Codes": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Location system
    "PM2": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Process manager
    "pnpm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Pocket": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Reading platform
    "Pocket Casts": ["Software Publishers", "Entertainment"],  # Podcast player
    "PocketBase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Backend platform
    "Podcast Addict": ["Software Publishers", "Entertainment"],  # Podcast player
    "Podcast Index": ["Internet Publishing and Broadcasting", "Entertainment"],  # Podcast directory
    "Podman": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container platform
    "Poe": ["Software Publishers", "Artificial Intelligence"],  # AI chat platform
    "Poetry": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Pointy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Retail platform
    "Polars": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data framework
    "Polestar": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Polkadot": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Blockchain platform
    "Poly": ["Computer and Electronic Product Manufacturing", "Communications Equipment Manufacturing"],  # Communication equipment
    "Polygon": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Blockchain platform
    "Polymer Project": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Polywork": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Professional network
    "Pond5": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Stock media
    "Pop!_OS": ["Software Publishers", "Operating Systems"],  # Operating system
    "Porkbun": ["Professional, Scientific, and Technical Services", "Domain Services"],  # Domain registrar
    "Porsche": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Portainer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container management
    "PortSwigger": ["Software Publishers", "Information Security"],  # Security tools
    "Posit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data science platform
    "PostCSS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS tool
    "PostgreSQL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "PostHog": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Postman": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API platform
    "Postmates": ["Transportation and Warehousing", "Food Services and Drinking Places"],  # Delivery service
    "POWERS": ["Beverage Manufacturing", "Distilleries"],  # Whiskey brand
    "pr.co": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # PR platform
    "pre-commit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Preact": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Prefect": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Workflow platform
    "Premier League": ["Arts, Entertainment, and Recreation", "Spectator Sports"],  # Sports league
    "PrepBytes": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "PrestaShop": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # E-commerce platform
    "Presto": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Query engine
    "Prettier": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code formatter
    "Pretzel": ["Software Publishers", "Entertainment"],  # Music licensing
    "Prevention": ["Internet Publishing and Broadcasting", "Publishing Industries"],  # Health magazine
    "Prezi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Presentation software
    "Prime": ["Retail Trade", "Nonstore Retailers"],  # Shopping service
    "Prime Video": ["Internet Publishing and Broadcasting", "Entertainment"],  # Streaming service
    "PrimeFaces": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "PrimeNG": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "PrimeReact": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "PrimeVue": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Printables": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # 3D model platform
    "Prisma": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database toolkit
    "Prismic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Private Division": ["Software Publishers", "Entertainment"],  # Game publisher
    "Private Internet Access": ["Software Publishers", "Information Security"],  # VPN service
    "Pro Tools": ["Software Publishers", "Entertainment"],  # Audio software
    "Probot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GitHub automation
    "Processing Foundation": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Creative coding
    "ProcessWire": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Product Hunt": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Product platform
    "Progate": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Progress": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tools
    "Prometheus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring system
    "Pronouns.page": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Identity platform
    "ProSieben": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV network
    "Proteus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Circuit design
    "Proto.io": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Prototyping platform
    "protocols.io": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Research platform
    "Proton": ["Software Publishers", "Information Security"],  # Privacy company
    "Proton Calendar": ["Software Publishers", "Information Security"],  # Calendar app
    "Proton Drive": ["Software Publishers", "Information Security"],  # Storage service
    "Proton Mail": ["Software Publishers", "Information Security"],  # Email service
    "Proton VPN": ["Software Publishers", "Information Security"],  # VPN service
    "ProtonDB": ["Internet Publishing and Broadcasting", "Entertainment"],  # Game compatibility
    "Protractor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Proxmox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Virtualization platform
    "Pterodactyl": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game server panel
    "PUBG": ["Software Publishers", "Entertainment"],  # Video game
    "Publons": ["Professional, Scientific, and Technical Services", "Research Organizations"],  # Research platform
    "PubMed": ["Professional, Scientific, and Technical Services", "Research Organizations"],  # Research database
    "Pug": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Template engine
    "Pulumi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Infrastructure tool
    "Puma": ["Manufacturing", "Footwear Manufacturing"],  # Sportswear manufacturer
    "Puppet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Configuration management
    "Puppeteer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Browser automation
    "PureScript": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "PurgeCSS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS tool
    "Purism": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Hardware manufacturer
    "Pushbullet": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Notification service
    "Pusher": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Real-time platform
    "PWA": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web technology
    "PyCharm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "PyCQA": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "Pydantic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data validation
    "PyG": ["Software Publishers", "Artificial Intelligence"],  # ML library
    "PyPI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package index
    "PyPy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Python implementation
    "PyScaffold": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project template
    "PySyft": ["Software Publishers", "Artificial Intelligence"],  # Privacy ML
    "Pytest": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Python": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "PythonAnywhere": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Hosting platform
    "PyTorch": ["Software Publishers", "Artificial Intelligence"],  # ML framework
    "PyUp": ["Software Publishers", "Information Security"],  # Security updates
    "Qantas": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Qase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Test management
    "Qatar Airways": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "qbittorrent": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File sharing
    "QEMU": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Emulator
    "Qgis": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GIS software
    "Qi": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Wireless charging
    "Qiita": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer platform
    "Qiskit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Quantum computing
    "QIWI": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment service
    "Qlik": ["Software Publishers", "Data Analytics"],  # Analytics platform
    "QMK": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Keyboard firmware
    "QNAP": ["Computer and Electronic Product Manufacturing", "Computer Storage Manufacturing"],  # Storage solutions
    "QQ": ["Software Publishers", "Social Networking Services"],  # Messaging platform
    "Qt": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development framework
    "Qualcomm": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor company
    "Qualtrics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Experience management
    "Qualys": ["Software Publishers", "Information Security"],  # Security platform
    "Quantcast": ["Software Publishers", "Advertising"],  # Advertising platform
    "QuantConnect": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Trading platform
    "Quarkus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Framework
    "Quarto": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Publishing system
    "Quasar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Qubes OS": ["Software Publishers", "Operating Systems"],  # Operating system
    "Quest": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IT management
    "QuickBooks": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Accounting software
    "QuickLook": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File preview
    "QuickTime": ["Software Publishers", "Entertainment"],  # Media player
    "quicktype": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code generation
    "Quip": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Collaboration software
    "Quizlet": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Quora": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Q&A platform
    "Qwant": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Search engine
    "Qwik": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Qwiklabs": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Qzone": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "R": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "R3": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain platform
    "RabbitMQ": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Message broker
    "Racket": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "RAD Studio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Radar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Location platform
    "radarr": ["Software Publishers", "Entertainment"],  # Media management
    "Radix UI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Railway": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Deployment platform
    "Rainmeter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Desktop customization
    "Rakuten": ["Internet Publishing and Broadcasting", "Retail Trade"],  # E-commerce platform
    "Ram": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Rancher": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container management
    "Rapid": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API platform
    "Rarible": ["Internet Publishing and Broadcasting", "Digital Assets"],  # NFT marketplace
    "Rasa": ["Software Publishers", "Artificial Intelligence"],  # Chatbot platform
    "Raspberry Pi": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Computer hardware
    "Ravelry": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Crafting community
    "Ray": ["Software Publishers", "Artificial Intelligence"],  # Distributed computing
    "Raycast": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Productivity tool
    "Raylib": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game framework
    "Razer": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Gaming hardware
    "Razorpay": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "Rclone": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File sync
    "React": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "React Bootstrap": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "React Hook Form": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Form library
    "React Query": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data fetching
    "React Router": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Routing library
    "React Table": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Table library
    "Reactive Resume": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Resume builder
    "ReactiveX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming library
    "ReactOS": ["Software Publishers", "Operating Systems"],  # Operating system
    "Read the Docs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation platform
    "Read.cv": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Resume platform
    "ReadMe": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation platform
    "Reason": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Reason Studios": ["Software Publishers", "Entertainment"],  # Music software
    "Recoil": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "Red": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Red Bull": ["Beverage Manufacturing", "Food Manufacturing"],  # Energy drinks
    "Red Candle Games": ["Software Publishers", "Entertainment"],  # Game developer
    "Red Hat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Enterprise software
    "Red Hat Open Shift": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container platform
    "Redash": ["Software Publishers", "Data Analytics"],  # Data visualization
    "Redbubble": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Marketplace platform
    "Reddit": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social platform
    "Redis": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Redmine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Redox": ["Software Publishers", "Operating Systems"],  # Operating system
    "Redragon": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Gaming hardware
    "Redsys": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment platform
    "Redux": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "Redux-Saga": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "RedwoodJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Reebok": ["Manufacturing", "Footwear Manufacturing"],  # Sportswear manufacturer
    "Refine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development framework
    "Refined GitHub": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Browser extension
    "Relay": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GraphQL framework
    "Reliance Industries Limited": ["Manufacturing", "Conglomerates"],  # Conglomerate
    "remark": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Markdown processor
    "Remedy Entertainment": ["Software Publishers", "Entertainment"],  # Game developer
    "Remix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "remove.bg": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image processing
    "Ren'Py": ["Software Publishers", "Entertainment"],  # Game engine
    "Renault": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Render": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Renovate": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Dependency management
    "Renren": ["Internet Publishing and Broadcasting", "Social Networking Services"],  # Social network
    "Replicate": ["Software Publishers", "Artificial Intelligence"],  # AI platform
    "Replit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Republic of Gamers": ["Computer and Electronic Product Manufacturing", "Computer Equipment Manufacturing"],  # Gaming hardware
    "ReScript": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "RescueTime": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Productivity tool
    "ResearchGate": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Research network
    "Resend": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email platform
    "ReSharper": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Resurrection Remix OS": ["Software Publishers", "Operating Systems"],  # Mobile OS
    "Retool": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Internal tools
    "RetroArch": ["Software Publishers", "Entertainment"],  # Emulation platform
    "RetroPie": ["Software Publishers", "Entertainment"],  # Gaming platform
    "ReVanced": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # App modification
    "reveal.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Presentation framework
    "ReverbNation": ["Internet Publishing and Broadcasting", "Entertainment"],  # Music platform
    "Revolt.chat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat platform
    "Revolut": ["Credit Intermediation and Related Activities", "Banking"],  # Digital bank
    "REWE": ["Food and Beverage Stores", "Retail Trade"],  # Supermarket chain
    "Rezgo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Booking software
    "Rhinoceros": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D software
    "Rich": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal formatting
    "Rider": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "Rimac Automobili": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "Rime": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Input method
    "Ring": ["Computer and Electronic Product Manufacturing", "Security Systems"],  # Smart home security
    "Riot Games": ["Software Publishers", "Entertainment"],  # Game developer
    "Ripple": ["Securities, Commodity Contracts, and Other Financial Investments", "Digital Assets"],  # Blockchain platform
    "RISC-V": ["Computer and Electronic Product Manufacturing", "Semiconductor Manufacturing"],  # Processor architecture
    "Riseup": ["Software Publishers", "Information Security"],  # Privacy services
    "Ritz Carlton": ["Accommodation", "Hotels and Motels"],  # Hotel chain
    "Rive": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Animation platform
    "roadmap.sh": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Roam Research": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Robinhood": ["Securities, Commodity Contracts, and Other Financial Investments", "Investment Services"],  # Trading platform
    "Roblox": ["Software Publishers", "Entertainment"],  # Gaming platform
    "Roblox Studio": ["Software Publishers", "Entertainment"],  # Game development
    "Roboflow": ["Software Publishers", "Artificial Intelligence"],  # Computer vision
    "Robot Framework": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Rocket": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Rocket.Chat": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat platform
    "RocksDB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Rockstar Games": ["Software Publishers", "Entertainment"],  # Game developer
    "Rockwell Automation": ["Manufacturing", "Industrial Automation"],  # Automation solutions
    "Rocky Linux": ["Software Publishers", "Operating Systems"],  # Operating system
    "Roku": ["Computer and Electronic Product Manufacturing", "Entertainment"],  # Streaming devices
    "Roll20": ["Software Publishers", "Entertainment"],  # Gaming platform
    "Rolls-Royce": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Automotive
    "rollup.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Rook": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Storage orchestrator
    "Roon": ["Software Publishers", "Entertainment"],  # Music software
    "Root Me": ["Educational Services", "Information Security"],  # Security challenges
    "Roots": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # WordPress tools
    "Roots Bedrock": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # WordPress framework
    "Roots Sage": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # WordPress theme
    "ROS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Robotics framework
    "Rossmann": ["Health and Personal Care Stores", "Retail Trade"],  # Drugstore chain
    "Rotary International": ["Religious, Grantmaking, Civic, Professional, and Similar Organizations", "Civic Organizations"],  # Service organization
    "Rotten Tomatoes": ["Internet Publishing and Broadcasting", "Entertainment"],  # Review aggregator
    "Roundcube": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email client
    "RSocket": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Protocol
    "RSS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Feed format
    "RStudio IDE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "RTÉ": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Broadcasting company
    "RTL": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Media company
    "RTLZWEI": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV channel
    "RTM": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit authority
    "RuboCop": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code linter
    "Ruby": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Ruby on Rails": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Ruby Sinatra": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "RubyGems": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "RubyMine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "Ruff": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code linter
    "Rumahweb": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "Rumble": ["Internet Publishing and Broadcasting", "Entertainment"],  # Video platform
    "Rundeck": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation platform
    "Runkeeper": ["Software Publishers", "Health Care and Social Assistance"],  # Fitness app
    "RunKit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code playground
    "Runrun.it": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Rust": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "RustDesk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Remote desktop
    "RxDB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Ryanair": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Rye": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "S7 Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Sabanci": ["Manufacturing", "Conglomerates"],  # Conglomerate
    "Safari": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "Sage": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "SageMath": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Math software
    "Sahibinden": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Marketplace platform
    "Sailfish OS": ["Software Publishers", "Operating Systems"],  # Mobile OS
    "Sails.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Salesforce": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CRM platform
    "Salla": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # E-commerce platform
    "Salt Project": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Configuration management
    "Sam's Club": ["General Merchandise Stores", "Retail Trade"],  # Retail chain
    "Samsung": ["Computer and Electronic Product Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "Samsung Pay": ["Credit Intermediation and Related Activities", "Professional, Scientific, and Technical Services"],  # Payment service
    "San Francisco Municipal Railway": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "SanDisk": ["Computer and Electronic Product Manufacturing", "Computer Storage Manufacturing"],  # Storage manufacturer
    "Sanic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Sanity": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Content platform
    "São Paulo Metro": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "SAP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Enterprise software
    "Sartorius": ["Manufacturing", "Laboratory Equipment Manufacturing"],  # Lab equipment manufacturer
    "Sass": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS preprocessor
    "Sat.1": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV channel
    "Satellite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software company
    "Saturn": ["Retail Trade", "Electronics and Appliance Stores"],  # Electronics retailer
    "Sauce Labs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing platform
    "Saudia": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Scala": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Scalar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software company
    "Scaleway": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud provider
    "Scania": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Vehicle manufacturer
    "Schneider Electric": ["Manufacturing", "Electrical Equipment Manufacturing"],  # Energy management
    "scikit-learn": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Machine learning library
    "Scilab": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Scientific software
    "SciPy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Scientific computing library
    "Scopus": ["Professional, Scientific, and Technical Services", "Information Services"],  # Research database
    "SCP Foundation": ["Internet Publishing and Broadcasting", "Entertainment"],  # Creative writing platform
    "Scrapbox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking platform
    "Scrapy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web scraping framework
    "Scratch": ["Software Publishers", "Educational Services"],  # Programming education
    "Screencastify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Screen recording
    "Scribd": ["Internet Publishing and Broadcasting", "Information Services"],  # Digital library
    "Scrimba": ["Educational Services", "Software Publishers"],  # Programming education
    "ScrollReveal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript library
    "Scrum Alliance": ["Professional, Scientific, and Technical Services", "Educational Services"],  # Agile certification
    "Scrutinizer CI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "ScyllaDB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Seagate": ["Computer and Electronic Product Manufacturing", "Computer Storage Manufacturing"],  # Storage manufacturer
    "SearXNG": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Search engine
    "SEAT": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "SeatGeek": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Ticket platform
    "SecurityScorecard": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # Security ratings
    "Sefaria": ["Internet Publishing and Broadcasting", "Educational Services"],  # Digital library
    "Sega": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game company
    "Selenium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Sellfy": ["Internet Publishing and Broadcasting", "E-commerce"],  # E-commerce platform
    "Semantic Scholar": ["Professional, Scientific, and Technical Services", "Information Services"],  # Research platform
    "Semantic UI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Semantic UI React": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Semantic Web": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web standards
    "semantic-release": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Release automation
    "Semaphore CI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Semrush": ["Professional, Scientific, and Technical Services", "Marketing Services"],  # Marketing platform
    "SemVer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version standard
    "Sencha": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript framework
    "SendGrid": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email service
    "Sennheiser": ["Manufacturing", "Audio Equipment Manufacturing"],  # Audio equipment
    "Sensu": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring platform
    "Sentry": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Error tracking
    "SEPA": ["Finance and Insurance", "Monetary Authorities-Central Bank"],  # Payment system
    "Sequelize": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database ORM
    "Server Fault": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Q&A platform
    "Serverless": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud computing
    "Session": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Sessionize": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Event platform
    "Setapp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software subscription
    "SFML": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Multimedia framework
    "shadcn/ui": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI components
    "Shadow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud gaming
    "Shanghai Metro": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "ShareX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Screen capture
    "sharp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image processing
    "Shazam": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Music recognition
    "Shell": ["Mining, Quarrying, and Oil and Gas Extraction", "Oil and Gas Extraction"],  # Oil company
    "Shelly": ["Manufacturing", "Electrical Equipment Manufacturing"],  # Smart home devices
    "Shenzhen Metro": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "Shields.io": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Badge service
    "Shikimori": ["Internet Publishing and Broadcasting", "Entertainment"],  # Anime platform
    "Shopee": ["Internet Publishing and Broadcasting", "E-commerce"],  # E-commerce platform
    "Shopify": ["Software Publishers", "E-commerce"],  # E-commerce platform
    "Shopware": ["Software Publishers", "E-commerce"],  # E-commerce platform
    "Shortcut": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Showpad": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Sales enablement
    "Showtime": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV network
    "Showwcase": ["Internet Publishing and Broadcasting", "Professional Networking"],  # Developer network
    "Shutterstock": ["Internet Publishing and Broadcasting", "Stock Photography"],  # Stock media
    "Sidekiq": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Job processing
    "SideQuest": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # VR platform
    "Siemens": ["Manufacturing", "Electrical Equipment Manufacturing"],  # Industrial manufacturing
    "SiFive": ["Manufacturing", "Semiconductor Manufacturing"],  # Chip design
    "Signal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Silver Airways": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Similarweb": ["Professional, Scientific, and Technical Services", "Marketing Services"],  # Web analytics
    "Simkl": ["Internet Publishing and Broadcasting", "Entertainment"],  # Media tracking
    "Simple Analytics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics
    "Simple Icons": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon library
    "SimpleLogin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email alias service
    "Simplenote": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "SimpleX": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging protocol
    "Sina Weibo": ["Internet Publishing and Broadcasting", "Social Media"],  # Social network
    "Singapore Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "SingleStore": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Sitecore": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "SitePoint": ["Internet Publishing and Broadcasting", "Educational Services"],  # Developer education
    "SiYuan": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking app
    "Skaffold": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Sketch": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Design software
    "Sketchfab": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # 3D model platform
    "SketchUp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D modeling
    "Skillshare": ["Educational Services", "Internet Publishing and Broadcasting"],  # Online learning
    "ŠKODA": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "Sky": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Media company
    "Skypack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript CDN
    "Slack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Communication platform
    "Slackware": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Slashdot": ["Internet Publishing and Broadcasting", "News and Media"],  # Tech news
    "SlickPic": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Photo sharing
    "Slides": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Presentation platform
    "SlideShare": ["Internet Publishing and Broadcasting", "Educational Services"],  # Content sharing
    "Slint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "smart": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "SmartThings": ["Manufacturing", "Home Automation"],  # IoT platform
    "Smashing Magazine": ["Internet Publishing and Broadcasting", "Educational Services"],  # Web development
    "SMRT": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "SmugMug": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Photo platform
    "Snapchat": ["Internet Publishing and Broadcasting", "Social Media"],  # Social media
    "Snapcraft": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Snapdragon": ["Manufacturing", "Semiconductor Manufacturing"],  # Mobile processors
    "SNCF": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Railway
    "Snort": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security tool
    "Snowflake": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data platform
    "Snowpack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "Snyk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security platform
    "Social Blade": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Analytics
    "Society6": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Art marketplace
    "Socket": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security tool
    "Socket.io": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # WebSocket framework
    "Softcatalà": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software localization
    "Softpedia": ["Internet Publishing and Broadcasting", "Software Distribution"],  # Software downloads
    "Sogou": ["Internet Publishing and Broadcasting", "Search Engines"],  # Search engine
    "Solana": ["Finance and Insurance", "Blockchain"],  # Blockchain platform
    "Solid": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript framework
    "Solidity": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Sololearn": ["Educational Services", "Software Publishers"],  # Learning platform
    "Solus": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Sonar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "SonarCloud": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code analysis
    "SonarLint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "SonarQube": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code quality
    "sonarr": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Media management
    "Sonatype": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software supply chain
    "Songkick": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Concert platform
    "Songoda": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game development
    "SonicWall": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cybersecurity
    "Sonos": ["Manufacturing", "Audio Equipment Manufacturing"],  # Audio equipment
    "Sony": ["Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "Soriana": ["Retail Trade", "General Merchandise Stores"],  # Retail chain
    "Soundcharts": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Music analytics
    "SoundCloud": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Music platform
    "Source Engine": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game engine
    "SourceForge": ["Internet Publishing and Broadcasting", "Software Distribution"],  # Software hosting
    "SourceHut": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development platform
    "Sourcetree": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git client
    "Southwest Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Spacemacs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "Spaceship": ["Finance and Insurance", "Investment Services"],  # Investment platform
    "SpaceX": ["Transportation and Warehousing", "Space Transportation"],  # Space company
    "spaCy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # NLP library
    "Spark AR": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # AR platform
    "Sparkasse": ["Finance and Insurance", "Banking"],  # Bank
    "SparkFun": ["Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "SparkPost": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email service
    "SPDX": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # License standard
    "Speaker Deck": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Presentation platform
    "Spectrum": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Community platform
    "Speedtest": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Internet testing
    "SpeedyPage": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web optimization
    "Sphere Online Judge": ["Educational Services", "Software Publishers"],  # Programming platform
    "Sphinx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation tool
    "SpigotMC": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game modding
    "Spine": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Animation software
    "Spinnaker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Deployment platform
    "Splunk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data platform
    "Spond": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Team management
    "Spotify": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Music streaming
    "Spotlight": ["Arts, Entertainment, and Recreation", "Professional, Scientific, and Technical Services"],  # Casting platform
    "Spreadshirt": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Custom apparel
    "Spreaker": ["Internet Publishing and Broadcasting", "Broadcasting"],  # Podcast platform
    "Spring": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development framework
    "Spring Boot": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development framework
    "Spring Security": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security framework
    "Spyder IDE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "SQLAlchemy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database toolkit
    "SQLite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database engine
    "Square": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment services
    "Square Enix": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game company
    "Squarespace": ["Software Publishers", "Internet Publishing and Broadcasting"],  # Website builder
    "SRG SSR": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Broadcasting corporation
    "SSRN": ["Professional, Scientific, and Technical Services", "Information Services"],  # Research network
    "SST": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development framework
    "Stack Exchange": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Q&A platform
    "Stack Overflow": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer platform
    "Stackbit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "StackBlitz": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "StackEdit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Markdown editor
    "StackHawk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security platform
    "StackShare": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Technology platform
    "Stadia": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Gaming platform
    "Staffbase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Employee communications
    "Stagetimer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Event timing
    "Standard Resume": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Resume platform
    "StandardJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript standard
    "Star Trek": ["Motion Picture and Sound Recording Industries", "Arts, Entertainment, and Recreation"],  # Entertainment franchise
    "Starbucks": ["Accommodation and Food Services", "Food Services and Drinking Places"],  # Coffee chain
    "Stardock": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Software company
    "Starling Bank": ["Finance and Insurance", "Banking"],  # Digital bank
    "Starship": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Shell prompt
    "start.gg": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Tournament platform
    "Startpage": ["Internet Publishing and Broadcasting", "Search Engines"],  # Search engine
    "STARZ": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Entertainment company
    "Statamic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Statista": ["Professional, Scientific, and Technical Services", "Information Services"],  # Statistics portal
    "Statuspage": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Status monitoring
    "Statuspal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Status monitoring
    "Steam": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Gaming platform
    "Steam Deck": ["Computer and Electronic Product Manufacturing", "Computer Hardware"],  # Gaming hardware
    "SteamDB": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Game database
    "Steamworks": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game development
    "Steelseries": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Gaming peripherals
    "Steem": ["Finance and Insurance", "Blockchain"],  # Blockchain platform
    "Steemit": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "Steinberg": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Audio software
    "Stellar": ["Finance and Insurance", "Blockchain"],  # Blockchain platform
    "Stencil": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Icon system
    "Stencyl": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game development
    "Stimulus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript framework
    "STMicroelectronics": ["Manufacturing", "Semiconductor Manufacturing"],  # Semiconductor manufacturer
    "StockX": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Marketplace platform
    "StopStalk": ["Internet Publishing and Broadcasting", "Educational Services"],  # Programming platform
    "Storyblok": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Storybook": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development tool
    "Strapi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Strava": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Fitness platform
    "Streamlabs": ["Software Publishers", "Broadcasting"],  # Streaming tools
    "Streamlit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # App framework
    "StreamRunners": ["Internet Publishing and Broadcasting", "Broadcasting"],  # Streaming platform
    "Stremio": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Media platform
    "Stripe": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment platform
    "strongSwan": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # VPN solution
    "Stryker": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "StubHub": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Ticket marketplace
    "Studio 3T": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database tool
    "styled-components": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS framework
    "stylelint": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS linter
    "StyleShare": ["Internet Publishing and Broadcasting", "Social Media"],  # Fashion platform
    "Stylus": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS preprocessor
    "Subaru": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "Sublime Text": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "Substack": ["Internet Publishing and Broadcasting", "Publishing Industries"],  # Publishing platform
    "Subtitle Edit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Subtitle editor
    "Subversion": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Version control
    "suckless": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software development
    "Sui": ["Finance and Insurance", "Blockchain"],  # Blockchain platform
    "Sumo Logic": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Suno": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # AI music
    "Sunrise": ["Telecommunications", "Telecommunications"],  # Telecom provider
    "Supabase": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database platform
    "Super User": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Q&A platform
    "Supercrease": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Fashion platform
    "Supermicro": ["Computer and Electronic Product Manufacturing", "Computer Hardware"],  # Server manufacturer
    "Surfshark": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # VPN service
    "SurrealDB": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "SurveyMonkey": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Survey platform
    "SUSE": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Suzuki": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Vehicle manufacturer
    "Svelte": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript framework
    "SVG": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Image format
    "SVG.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics library
    "SVGO": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # SVG optimizer
    "SvgTrace": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # SVG tool
    "Swagger": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API documentation
    "Swarm": ["Internet Publishing and Broadcasting", "Social Media"],  # Location platform
    "Sway": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Window manager
    "SWC": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript compiler
    "Swift": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Swiggy": ["Internet Publishing and Broadcasting", "Food Services and Drinking Places"],  # Food delivery
    "Swiper": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript library
    "SWR": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data fetching
    "Symantec": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security software
    "Symbolab": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Math tool
    "Symfony": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # PHP framework
    "Symphony": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Communication platform
    "SymPy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Math library
    "Syncthing": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File sync
    "Synology": ["Computer and Electronic Product Manufacturing", "Computer Storage Manufacturing"],  # Storage solutions
    "System76": ["Computer and Electronic Product Manufacturing", "Computer Hardware"],  # Computer manufacturer
    "Tabelog": ["Internet Publishing and Broadcasting", "Food Services and Drinking Places"],  # Restaurant platform
    "TableCheck": ["Software Publishers", "Food Services and Drinking Places"],  # Restaurant platform
    "Taco Bell": ["Food Services and Drinking Places", "Food Services and Drinking Places"],  # Restaurant chain
    "tado°": ["Manufacturing", "Home Automation"],  # Smart home
    "Taichi Graphics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics framework
    "Taichi Lang": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Tails": ["Software Publishers", "Operating Systems"],  # Operating system
    "Tailscale": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # VPN platform
    "Tailwind CSS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS framework
    "Taipy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Take-Two Interactive Software": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game publisher
    "Talend": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data integration
    "Talenthouse": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Creative platform
    "Talos": ["Software Publishers", "Operating Systems"],  # Operating system
    "Tamiya": ["Manufacturing", "Miscellaneous Manufacturing"],  # Model manufacturer
    "Tampermonkey": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Browser extension
    "Taobao": ["Internet Publishing and Broadcasting", "E-commerce"],  # E-commerce platform
    "Tapas": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Digital content
    "Target": ["Retail Trade", "General Merchandise Stores"],  # Retail chain
    "TAROM": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Task": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Task runner
    "Tasmota": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IoT firmware
    "Tata": ["Manufacturing", "Conglomerates"],  # Conglomerate
    "Tata Consultancy Services": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "Tauri": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # App framework
    "TaxBuzz": ["Professional, Scientific, and Technical Services", "Tax Services"],  # Tax platform
    "Teal": ["Professional, Scientific, and Technical Services", "Management Services"],  # Career platform
    "TeamCity": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "TeamSpeak": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Voice chat
    "TeamViewer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Remote access
    "TechCrunch": ["Internet Publishing and Broadcasting", "News and Media"],  # Tech news
    "TED": ["Educational Services", "Internet Publishing and Broadcasting"],  # Educational content
    "TeePublic": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Custom apparel
    "Teespring": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Custom merchandise
    "Tekton": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD framework
    "TELE 5": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV channel
    "Télé-Québec": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # TV network
    "Telefónica": ["Telecommunications", "Telecommunications"],  # Telecom provider
    "Telegram": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging platform
    "Telegraph": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Publishing platform
    "Temporal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Workflow platform
    "TensorFlow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML framework
    "Teradata": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database platform
    "teratail": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Q&A platform
    "Termius": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal client
    "Terraform": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Infrastructure tool
    "Tesco": ["Retail Trade", "General Merchandise Stores"],  # Retail chain
    "Tesla": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "TestCafe": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Testin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing platform
    "Testing Library": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "TestRail": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Test management
    "Tether": ["Finance and Insurance", "Blockchain"],  # Cryptocurrency
    "Textpattern": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "TGA": ["Arts, Entertainment, and Recreation", "Broadcasting"],  # Awards show
    "Thangs": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # 3D model platform
    "Thanos": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring system
    "The Algorithms": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Algorithm repository
    "The Boring Company": ["Heavy and Civil Engineering Construction", "Transportation"],  # Infrastructure company
    "The Conversation": ["Internet Publishing and Broadcasting", "News and Media"],  # News platform
    "THE FINALS": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Video game
    "The Guardian": ["Internet Publishing and Broadcasting", "News and Media"],  # News organization
    "The Irish Times": ["Internet Publishing and Broadcasting", "News and Media"],  # News organization
    "The Mighty": ["Internet Publishing and Broadcasting", "Health Care and Social Assistance"],  # Health community
    "The Models Resource": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Game assets
    "The Movie Database": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Movie database
    "The North Face": ["Manufacturing", "Apparel Manufacturing"],  # Outdoor apparel
    "The Odin Project": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Programming education
    "The Register": ["Internet Publishing and Broadcasting", "News and Media"],  # Tech news
    "The Sounds Resource": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Game assets
    "The Spriters Resource": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Game assets
    "The Washington Post": ["Internet Publishing and Broadcasting", "News and Media"],  # News organization
    "The Weather Channel": ["Broadcasting", "Information Services"],  # Weather service
    "Thingiverse": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # 3D printing platform
    "ThinkPad": ["Computer and Electronic Product Manufacturing", "Computer Hardware"],  # Computer hardware
    "thirdweb": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web3 platform
    "Threadless": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Custom apparel
    "Threads": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "Three.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D library
    "Threema": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging app
    "Thumbtack": ["Internet Publishing and Broadcasting", "Professional Services"],  # Service marketplace
    "Thunderbird": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email client
    "Thunderstore": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Mod platform
    "Thurgauer Kantonalbank": ["Finance and Insurance", "Banking"],  # Bank
    "Thymeleaf": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Template engine
    "Ticketmaster": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Ticket platform
    "TickTick": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Task management
    "Tidal": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Music streaming
    "TiddlyWiki": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking
    "Tide": ["Finance and Insurance", "Banking"],  # Banking platform
    "Tidyverse": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data science tools
    "TietoEVRY": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "TikTok": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "Tilda Publishing": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "Tile": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Tracking devices
    "Timescale": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database
    "Tina": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS framework
    "Tinder": ["Internet Publishing and Broadcasting", "Social Media"],  # Dating platform
    "Tindie": ["Internet Publishing and Broadcasting", "Electronics and Appliance Stores"],  # Electronics marketplace
    "Tinkercad": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D design
    "tinygrad": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML framework
    "TinyLetter": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Newsletter platform
    "Tistory": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Blogging platform
    "tldraw": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Drawing tool
    "tmux": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal multiplexer
    "Todoist": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Task management
    "Toggl": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Time tracking
    "Toggl Track": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Time tracking
    "Tokyo Metro": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit system
    "Toll": ["Transportation and Warehousing", "Truck Transportation"],  # Logistics company
    "TOML": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data format
    "Tomorrowland": ["Arts, Entertainment, and Recreation", "Performing Arts"],  # Music festival
    "TomTom": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Navigation technology
    "TON": ["Finance and Insurance", "Blockchain"],  # Blockchain platform
    "Top.gg": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Bot platform
    "Topcoder": ["Professional, Scientific, and Technical Services", "Software Development"],  # Programming platform
    "Toptal": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Talent platform
    "Tor Browser": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Privacy browser
    "Tor Project": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Privacy network
    "Torizon": ["Software Publishers", "Operating Systems"],  # Operating system
    "Toshiba": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Electronics manufacturer
    "TOTVS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Enterprise software
    "TourBox": ["Computer and Electronic Product Manufacturing", "Computer Hardware"],  # Input device
    "Tower": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Git client
    "Toyota": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "TP-Link": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Networking equipment
    "tqdm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Progress bar library
    "Traccar": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # GPS tracking
    "TradingView": ["Finance and Insurance", "Securities and Financial Investment"],  # Trading platform
    "Traefik Mesh": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Service mesh
    "Traefik Proxy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Proxy server
    "Trailforks": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Trail database
    "TrainerRoad": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Cycling platform
    "Trakt": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Media tracking
    "Transifex": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Localization platform
    "Transmission": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Torrent client
    "Transport for Ireland": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit authority
    "Transport for London": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Transit authority
    "Travis CI": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CI/CD platform
    "Treehouse": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Trello": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Project management
    "Trend Micro": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security software
    "Treyarch": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game developer
    "Tricentis": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing platform
    "Trilium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Note-taking
    "Triller": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "TrillerTV": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Streaming platform
    "Trimble": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # Technology solutions
    "Trino": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Query engine
    "Trip.com": ["Internet Publishing and Broadcasting", "Travel Services"],  # Travel platform
    "Tripadvisor": ["Internet Publishing and Broadcasting", "Travel Services"],  # Travel platform
    "trivago": ["Internet Publishing and Broadcasting", "Travel Services"],  # Hotel search
    "Trivy": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security scanner
    "Trove": ["Professional, Scientific, and Technical Services", "Libraries and Archives"],  # Digital library
    "tRPC": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # API framework
    "TrueNAS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Storage platform
    "TrueUp": ["Professional, Scientific, and Technical Services", "Information Services"],  # Tech analytics
    "trulia": ["Internet Publishing and Broadcasting", "Real Estate"],  # Real estate platform
    "Trusted Shops": ["Professional, Scientific, and Technical Services", "E-commerce"],  # Trust platform
    "Trustpilot": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Review platform
    "Try It Online": ["Software Publishers", "Educational Services"],  # Code playground
    "TryHackMe": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Security training
    "ts-node": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # TypeScript runtime
    "Tubi": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Streaming service
    "TUI": ["Transportation and Warehousing", "Travel Services"],  # Travel company
    "Tumblr": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "TuneIn": ["Internet Publishing and Broadcasting", "Broadcasting"],  # Radio platform
    "Turbo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Turborepo": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build system
    "TurboSquid": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # 3D model marketplace
    "Turkish Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Turso": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database platform
    "Tuta": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Email service
    "TV Time": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # TV tracking
    "TV4 Play": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Streaming service
    "Twilio": ["Software Publishers", "Telecommunications"],  # Communications platform
    "Twinkly": ["Manufacturing", "Electrical Equipment Manufacturing"],  # Smart lighting
    "Twinmotion": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D visualization
    "Twitch": ["Internet Publishing and Broadcasting", "Broadcasting"],  # Streaming platform
    "Typeform": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Form builder
    "TypeORM": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database framework
    "Typer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CLI framework
    "TypeScript": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "TYPO3": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Typst": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Typesetting system
    "U.S. News": ["Internet Publishing and Broadcasting", "News and Media"],  # News organization
    "Uber": ["Transportation and Warehousing", "Transit and Ground Passenger Transportation"],  # Ride-hailing
    "Uber Eats": ["Internet Publishing and Broadcasting", "Food Services and Drinking Places"],  # Food delivery
    "Ubiquiti": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Networking equipment
    "Ubisoft": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game publisher
    "uBlock Origin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Ad blocker
    "Ubuntu": ["Software Publishers", "Operating Systems"],  # Operating system
    "Ubuntu MATE": ["Software Publishers", "Operating Systems"],  # Operating system
    "Udacity": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Udemy": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "UFC": ["Arts, Entertainment, and Recreation", "Performing Arts"],  # Sports organization
    "UIkit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "UiPath": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation platform
    "UKCA": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Certification mark
    "Ultralytics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # AI platform
    "Ulule": ["Internet Publishing and Broadcasting", "Crowdfunding"],  # Crowdfunding platform
    "Umami": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Analytics platform
    "Umbraco": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "UML": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Modeling language
    "Unacademy": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Under Armour": ["Manufacturing", "Apparel Manufacturing"],  # Sportswear manufacturer
    "Underscore.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript library
    "Undertale": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Video game
    "Unicode": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # Character encoding
    "Unilever": ["Manufacturing", "Consumer Goods Manufacturing"],  # Consumer goods
    "Uniqlo": ["Retail Trade", "Clothing and Clothing Accessories Stores"],  # Clothing retailer
    "United Airlines": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "United Nations": ["Public Administration", "International Affairs"],  # International organization
    "Unity": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game engine
    "UnJS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript tools
    "Unlicense": ["Professional, Scientific, and Technical Services", "Standards Organizations"],  # License
    "UnoCSS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CSS framework
    "unpkg": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package CDN
    "Unraid": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Server OS
    "Unreal Engine": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game engine
    "Unsplash": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Photo platform
    "Untappd": ["Internet Publishing and Broadcasting", "Food Services and Drinking Places"],  # Beer platform
    "UpCloud": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud provider
    "Uphold": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Financial platform
    "UpLabs": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Design marketplace
    "Upptime": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring system
    "UPS": ["Transportation and Warehousing", "Couriers and Messengers"],  # Shipping company
    "Upstash": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database platform
    "Uptime Kuma": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring system
    "Upwork": ["Professional, Scientific, and Technical Services", "Employment Services"],  # Freelance platform
    "USPS": ["Transportation and Warehousing", "Postal Service"],  # Postal service
    "uTorrent": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Torrent client
    "uv": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "V": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "v0": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # AI development
    "V2EX": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech community
    "V8": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # JavaScript engine
    "Vaadin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Vagrant": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "Vala": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Valorant": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Video game
    "Valve": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Game company
    "Vapor": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Vault": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security platform
    "Vaultwarden": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Password manager
    "Vauxhall": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "vBulletin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Forum software
    "Vectary": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # 3D design platform
    "Vector Logo Zone": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Logo database
    "Vectorworks": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CAD software
    "Veeam": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Backup software
    "VEED": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video editing
    "Veepee": ["Internet Publishing and Broadcasting", "Retail Trade"],  # E-commerce platform
    "Vega": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Visualization library
    "VEGAS": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video editing
    "Velocity": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Game server
    "Velog": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Blogging platform
    "Vencord": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Discord client
    "Venmo": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment service
    "Vercel": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Verdaccio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package registry
    "Veritas": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Enterprise software
    "Verizon": ["Telecommunications", "Telecommunications"],  # Telecom provider
    "Vespa": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Scooter manufacturer
    "Vestel": ["Manufacturing", "Electronics Manufacturing"],  # Electronics manufacturer
    "VEXXHOST": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud provider
    "vFairs": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Virtual events
    "Viadeo": ["Internet Publishing and Broadcasting", "Professional Networking"],  # Professional network
    "Viaplay": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Streaming service
    "Viber": ["Software Publishers", "Telecommunications"],  # Messaging app
    "Viblo": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech community
    "VictoriaMetrics": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Monitoring system
    "Victron Energy": ["Manufacturing", "Electrical Equipment Manufacturing"],  # Energy systems
    "Vim": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Text editor
    "Vimeo": ["Internet Publishing and Broadcasting", "Motion Picture and Sound Recording Industries"],  # Video platform
    "Vimeo Livestream": ["Internet Publishing and Broadcasting", "Broadcasting"],  # Streaming platform
    "Virgin": ["Management of Companies and Enterprises", "Conglomerates"],  # Conglomerate
    "Virgin Atlantic": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Virgin Media": ["Telecommunications", "Telecommunications"],  # Telecom provider
    "VirtualBox": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Virtualization
    "VirusTotal": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security platform
    "Visa": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment network
    "visx": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Visualization library
    "Vite": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "VitePress": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Documentation tool
    "Vitess": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Database clustering
    "Vitest": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Viva Wallet": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment platform
    "Vivaldi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web browser
    "Vivino": ["Internet Publishing and Broadcasting", "Food Services and Drinking Places"],  # Wine platform
    "Vivint": ["Manufacturing", "Home Automation"],  # Smart home
    "vivo": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Smartphone manufacturer
    "VK": ["Internet Publishing and Broadcasting", "Social Media"],  # Social network
    "VLC media player": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Media player
    "VMware": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Virtualization
    "Vodafone": ["Telecommunications", "Telecommunications"],  # Telecom provider
    "Void Linux": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "VoIP.ms": ["Telecommunications", "Telecommunications"],  # VoIP provider
    "Volkswagen": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "Volvo": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Car manufacturer
    "Vonage": ["Telecommunications", "Telecommunications"],  # Communications provider
    "Voron Design": ["Manufacturing", "3D Printing"],  # 3D printer design
    "Vowpal Wabbit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Machine learning
    "VOX": ["Internet Publishing and Broadcasting", "News and Media"],  # News organization
    "VRChat": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Virtual reality
    "VSCO": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Photo editing
    "VSCodium": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code editor
    "VTEX": ["Software Publishers", "E-commerce"],  # E-commerce platform
    "Vue.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Vuetify": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # UI framework
    "Vulkan": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics API
    "Vultr": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud provider
    "Vyond": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Animation platform
    "W3Schools": ["Educational Services", "Professional, Scientific, and Technical Services"],  # Learning platform
    "Wacom": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Input devices
    "Wagmi": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web3 library
    "Wagtail": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Wails": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Desktop framework
    "WakaTime": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Time tracking
    "WALKMAN": ["Manufacturing", "Consumer Electronics"],  # Audio player
    "Wallabag": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Reading platform
    "WalletConnect": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain protocol
    "Walmart": ["Retail Trade", "General Merchandise Stores"],  # Retail chain
    "Wantedly": ["Internet Publishing and Broadcasting", "Professional Networking"],  # Job platform
    "Wappalyzer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Technology profiler
    "Warner Bros.": ["Motion Picture and Sound Recording Industries", "Entertainment"],  # Entertainment company
    "Warp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal emulator
    "Wasabi": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud storage
    "wasmCloud": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Wasmer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Runtime platform
    "Watchtower": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Container updater
    "Wattpad": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Story platform
    "Wayland": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Display server
    "Waze": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Navigation app
    "WazirX": ["Finance and Insurance", "Securities and Financial Investment"],  # Cryptocurrency exchange
    "Wear OS": ["Software Publishers", "Operating Systems"],  # Operating system
    "Weasyl": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Art platform
    "WEB.DE": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Web portal
    "Web3.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blockchain library
    "WebAssembly": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web standard
    "WebAuthn": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Authentication standard
    "webcomponents.org": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web components
    "WebdriverIO": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Testing framework
    "Webex": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Communication platform
    "Webflow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "WebGL": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics API
    "WebGPU": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics API
    "Weblate": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Translation platform
    "Webmin": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Server management
    "WebMoney": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment system
    "Webpack": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Build tool
    "WebRTC": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Communication protocol
    "WebStorm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IDE
    "WEBTOON": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Comics platform
    "webtrees": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Genealogy software
    "WeChat": ["Software Publishers", "Social Media"],  # Messaging platform
    "WeGame": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Gaming platform
    "Weights & Biases": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML platform
    "Welcome to the Jungle": ["Internet Publishing and Broadcasting", "Employment Services"],  # Job platform
    "Wellfound": ["Internet Publishing and Broadcasting", "Employment Services"],  # Startup platform
    "Wells Fargo": ["Finance and Insurance", "Banking"],  # Bank
    "WEMO": ["Manufacturing", "Home Automation"],  # Smart home
    "Western Digital": ["Manufacturing", "Computer Storage Manufacturing"],  # Storage manufacturer
    "Western Union": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Money transfer
    "WeTransfer": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # File transfer
    "WezTerm": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Terminal emulator
    "wgpu": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Graphics API
    "WhatsApp": ["Software Publishers", "Social Media"],  # Messaging platform
    "When I Work": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Scheduling platform
    "wiki.gg": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Wiki platform
    "Wiki.js": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Wiki platform
    "Wikibooks": ["Internet Publishing and Broadcasting", "Educational Services"],  # Educational content
    "Wikidata": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Knowledge base
    "Wikimedia Commons": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Media repository
    "Wikimedia Foundation": ["Professional, Scientific, and Technical Services", "Nonprofit Organization"],  # Nonprofit
    "Wikipedia": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Encyclopedia
    "Wikiquote": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Quote collection
    "Wikiversity": ["Internet Publishing and Broadcasting", "Educational Services"],  # Educational platform
    "Wikivoyage": ["Internet Publishing and Broadcasting", "Travel Services"],  # Travel guide
    "Winamp": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Media player
    "Wine": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Compatibility layer
    "Wipro": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "Wire": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Messaging platform
    "WireGuard": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # VPN protocol
    "Wireshark": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Network analyzer
    "Wise": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Money transfer
    "Wish": ["Internet Publishing and Broadcasting", "E-commerce"],  # E-commerce platform
    "Wistia": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video platform
    "Wix": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Website builder
    "Wizz Air": ["Transportation and Warehousing", "Air Transportation"],  # Airline
    "Wolfram": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Technology company
    "Wolfram Language": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Wolfram Mathematica": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Technical computing
    "Wondershare": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Software company
    "Wondershare Filmora": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video editor
    "Woo": ["Software Publishers", "E-commerce"],  # E-commerce platform
    "WooCommerce": ["Software Publishers", "E-commerce"],  # E-commerce platform
    "WordPress": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # CMS platform
    "Workplace": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Collaboration platform
    "World Health Organization": ["Public Administration", "International Affairs"],  # Health organization
    "WP Engine": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Web hosting
    "WP Rocket": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # WordPress plugin
    "WPExplorer": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # WordPress themes
    "Write.as": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Blogging platform
    "WWE": ["Arts, Entertainment, and Recreation", "Performing Arts"],  # Entertainment company
    "Wwise": ["Software Publishers", "Arts, Entertainment, and Recreation"],  # Audio middleware
    "WXT": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Browser extension
    "Wykop": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "Wyze": ["Manufacturing", "Home Automation"],  # Smart home
    "X": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "X.Org": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Display server
    "XAMPP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "Xcode": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Development environment
    "XDA Developers": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Developer community
    "Xendit": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment platform
    "Xero": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Accounting software
    "XFCE": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Desktop environment
    "Xiaohongshu": ["Internet Publishing and Broadcasting", "Social Media"],  # Social platform
    "Xiaomi": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Electronics manufacturer
    "Xing": ["Internet Publishing and Broadcasting", "Professional Networking"],  # Professional network
    "XML": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Markup language
    "XMPP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Communication protocol
    "XO": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code linter
    "XRP": ["Finance and Insurance", "Blockchain"],  # Cryptocurrency
    "XSplit": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Streaming software
    "XState": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # State management
    "Xubuntu": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "xyflow": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Flow visualization
    "Y Combinator": ["Professional, Scientific, and Technical Services", "Investment Services"],  # Startup accelerator
    "yabai": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Window manager
    "Yale": ["Educational Services", "Educational Services"],  # University
    "Yamaha Corporation": ["Manufacturing", "Musical Instrument Manufacturing"],  # Musical instruments
    "Yamaha Motor Corporation": ["Transportation Equipment Manufacturing", "Motor Vehicle Manufacturing"],  # Vehicle manufacturer
    "YAML": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Data format
    "Yandex Cloud": ["Data Processing, Hosting, and Related Services", "Professional, Scientific, and Technical Services"],  # Cloud platform
    "Yarn": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Package manager
    "Yelp": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Review platform
    "Yeti": ["Manufacturing", "Consumer Goods Manufacturing"],  # Outdoor products
    "Yii": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web framework
    "Yoast": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # SEO platform
    "YOLO": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # ML framework
    "YouHodler": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Crypto platform
    "YouTube": ["Internet Publishing and Broadcasting", "Broadcasting"],  # Video platform
    "YouTube Gaming": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Gaming platform
    "YouTube Kids": ["Internet Publishing and Broadcasting", "Educational Services"],  # Children's content
    "YouTube Music": ["Internet Publishing and Broadcasting", "Arts, Entertainment, and Recreation"],  # Music platform
    "YouTube Shorts": ["Internet Publishing and Broadcasting", "Social Media"],  # Short-form video
    "YouTube Studio": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Creator tools
    "YouTube TV": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Streaming service
    "Yr": ["Internet Publishing and Broadcasting", "Information Services"],  # Weather service
    "Yubico": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Security keys
    "YunoHost": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Server platform
    "Żabka": ["Retail Trade", "Food and Beverage Stores"],  # Retail chain
    "Zaim": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Finance management
    "Zalando": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Fashion retailer
    "Zalo": ["Software Publishers", "Social Media"],  # Messaging platform
    "ZAP": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Security tool
    "Zapier": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Automation platform
    "Zara": ["Retail Trade", "Clothing and Clothing Accessories Stores"],  # Fashion retailer
    "Zazzle": ["Internet Publishing and Broadcasting", "Retail Trade"],  # Custom products
    "Zcash": ["Finance and Insurance", "Blockchain"],  # Cryptocurrency
    "ZCOOL": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Design platform
    "ZDF": ["Broadcasting", "Motion Picture and Sound Recording Industries"],  # Broadcaster
    "ZebPay": ["Finance and Insurance", "Securities and Financial Investment"],  # Crypto exchange
    "Zebra Technologies": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # Enterprise hardware
    "Zed Industries": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Code editor
    "Zelle": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment service
    "Zend": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # PHP framework
    "Zendesk": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Customer service
    "Zenn": ["Internet Publishing and Broadcasting", "Professional, Scientific, and Technical Services"],  # Tech platform
    "Zenodo": ["Professional, Scientific, and Technical Services", "Information Services"],  # Research repository
    "Zensar": ["Professional, Scientific, and Technical Services", "Computer Systems Design"],  # IT services
    "Zerodha": ["Finance and Insurance", "Securities and Financial Investment"],  # Trading platform
    "ZeroTier": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Networking platform
    "Zettlr": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Writing tool
    "Zhihu": ["Internet Publishing and Broadcasting", "Social Media"],  # Q&A platform
    "Zig": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Programming language
    "Zigbee": ["Manufacturing", "Computer and Electronic Product Manufacturing"],  # IoT protocol
    "Zigbee2MQTT": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # IoT software
    "Ziggo": ["Telecommunications", "Telecommunications"],  # Telecom provider
    "Zilch": ["Finance and Insurance", "Credit Intermediation and Related Activities"],  # Payment platform
    "Zillow": ["Internet Publishing and Broadcasting", "Real Estate"],  # Real estate platform
    "ZincSearch": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Search engine
    "Zingat": ["Internet Publishing and Broadcasting", "Real Estate"],  # Real estate platform
    "Zod": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Type checking
    "Zoho": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Business software
    "Zoiper": ["Software Publishers", "Telecommunications"],  # VoIP software
    "Zomato": ["Internet Publishing and Broadcasting", "Food Services and Drinking Places"],  # Food delivery
    "Zoom": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Video conferencing
    "Zorin": ["Software Publishers", "Operating Systems"],  # Linux distribution
    "Zotero": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Research tool
    "Zsh": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Shell
    "Zulip": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Chat platform
    "Zyte": ["Software Publishers", "Professional, Scientific, and Technical Services"],  # Web scraping
}

def update_json_with_industries(input_file, output_file):
    # Read the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    
    # Keep track of changes
    updates_made = 0
    entries_skipped = 0
    
    # Update each entry with industry field after hex
    for item in data:
        title = item['title']
        # Skip if already has industry field
        if 'industry' in item:
            entries_skipped += 1
            continue
            
        if title in INDUSTRY_MAPPINGS:
            # Create new OrderedDict with industry field after hex
            new_item = OrderedDict()
            for key, value in item.items():
                new_item[key] = value
                if key == 'hex':
                    new_item['industry'] = INDUSTRY_MAPPINGS[title]
            # Replace old item with new item
            item.clear()
            item.update(new_item)
            updates_made += 1
    
    # Write back to file with proper formatting
    with open(output_file, 'w') as f:
        json.dump(data, f, indent='\t')
    
    print(f"Processing complete:")
    print(f"- {updates_made} entries updated with industry tags")
    print(f"- {entries_skipped} entries skipped (already had industry tags)")

if __name__ == "__main__":
    input_file = "_data/simple-icons.json"
    output_file = "_data/simple-icons.json"
    update_json_with_industries(input_file, output_file) 