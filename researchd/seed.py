from flask.cli import with_appcontext
from researchd import db
from researchd.models import User, Profile, Education, Experience, File, Photo, Social, Publication
import click

@click.command("seed")
@with_appcontext
def seed():
    # Clears existing data
    db.drop_all()
    db.create_all()

    # Create sample user
    alice = User(
        email="alice@example.com",
        first_name="Alice",
        last_name="Smith",
    )
    alice.set_password("password123")
    db.session.add(alice)
    db.session.commit()

    alice_profile = Profile(
        user_id=alice.id,
        title="Professor of Biology",
        institution="Example University",
        department="Biology",
        bio="Researcher in molecular biology",
        pfp="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHEJ-8GyKlZr5ZmEfRMmt5nR4tH_aP-crbgg&s",
        location="Perth"
    )
    db.session.add(alice_profile)
    db.session.commit()

    alice_edu = Education(
        pid=alice_profile.pid,
        degree="PhD in Biology",
        institution="University of Western Australia",
        start_year=2005,
        end_year=2010
    )
    db.session.add(alice_edu)

    alice_exp = Experience(
        pid=alice_profile.pid,
        role="Research Scientist",
        institution="BioLabs Inc.",
        start_year=2010,
        end_year=2015
    )
    db.session.add(alice_exp)

    alice_file = File(
        pid=alice_profile.pid,
        file_name="research_paper.pdf",
        file_type="pdf",
        file_size=123456,
        file_path="https://frazer.uq.edu.au/files/3190/MolBiolWS01DNATech.pdf"
    )
    db.session.add(alice_file)
    db.session.commit()

    alice_pub = Publication(
        pid=alice_profile.pid,
        title="Groundbreaking Research",
        journal="Science Journal",
        year=2020,
        doi="10.1234/example.doi",
        url="https://doi.org/10.1234/example.doi",
        fid=alice_file.fid
    )
    db.session.add(alice_pub)

    alice_photo = Photo(
        pid=alice_profile.pid,
        file_path="https://media.istockphoto.com/id/1089913166/photo/female-medical-researcher.jpg",
        caption="Alice in a lab"
    )
    db.session.add(alice_photo)

    alice_social = Social(
        pid=alice_profile.pid,
        platform="Twitter",
        url="https://twitter.com/alice"
    )
    db.session.add(alice_social)

    # Additional users data
    users_data = [
        {
            "user": {
                "email": "david@example.com",
                "first_name": "David",
                "last_name": "Chen",
                "password": "password123"
            },
            "profile": {
                "title": "Associate Professor of Computer Science",
                "institution": "University of Technology Sydney",
                "department": "Computer Science",
                "bio": "AI researcher specializing in machine learning and natural language processing. Passionate about making AI more accessible and ethical.",
                "pfp": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
                "location": "Sydney, Australia",
                "research_interests": "Machine Learning, Natural Language Processing, AI Ethics, Deep Learning"
            },
            "education": [
                {"degree": "PhD in Computer Science", "institution": "Stanford University", "start_year": 2012, "end_year": 2017},
                {"degree": "Bachelor of Engineering", "institution": "University of New South Wales", "start_year": 2008, "end_year": 2012}
            ],
            "experience": [
                {"role": "Senior Research Scientist", "institution": "Google Research", "start_year": 2017, "end_year": 2021},
                {"role": "Assistant Professor", "institution": "University of Technology Sydney", "start_year": 2021, "end_year": None}
            ],
            "publications": [
                {"title": "Ethical AI: A Framework for Responsible Development", "journal": "Nature Machine Intelligence", "year": 2023, "doi": "10.1038/s42256-023-00684-2"},
                {"title": "Large Language Models and Their Applications", "journal": "Communications of the ACM", "year": 2022, "doi": "10.1145/3571721"}
            ],
            "socials": [
                {"platform": "GitHub", "url": "https://github.com/davidchen-ai"},
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/david-chen-ai"}
            ]
        },
        {
            "user": {
                "email": "maria@example.com",
                "first_name": "Maria",
                "last_name": "Rodriguez",
                "password": "password123"
            },
            "profile": {
                "title": "Research Fellow in Environmental Science",
                "institution": "Australian National University",
                "department": "Environmental Science",
                "bio": "Environmental scientist focused on climate change impacts and sustainable solutions. Working on innovative approaches to environmental monitoring and conservation.",
                "pfp": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
                "location": "Canberra, Australia",
                "research_interests": "Climate Change, Environmental Monitoring, Sustainability, Conservation Biology"
            },
            "education": [
                {"degree": "PhD in Environmental Science", "institution": "Australian National University", "start_year": 2016, "end_year": 2020},
                {"degree": "Master of Environmental Management", "institution": "University of Queensland", "start_year": 2014, "end_year": 2016}
            ],
            "experience": [
                {"role": "Research Assistant", "institution": "CSIRO", "start_year": 2020, "end_year": 2022},
                {"role": "Research Fellow", "institution": "Australian National University", "start_year": 2022, "end_year": None}
            ],
            "publications": [
                {"title": "Climate Change Impacts on Australian Ecosystems", "journal": "Global Change Biology", "year": 2023, "doi": "10.1111/gcb.16789"},
                {"title": "Sustainable Monitoring Technologies", "journal": "Environmental Science & Technology", "year": 2022, "doi": "10.1021/acs.est.2c04567"}
            ],
            "socials": [
                {"platform": "Twitter", "url": "https://twitter.com/maria_env_sci"},
                {"platform": "ResearchGate", "url": "https://researchgate.net/profile/Maria-Rodriguez-Environmental"}
            ]
        },
        {
            "user": {
                "email": "james@example.com",
                "first_name": "James",
                "last_name": "Wilson",
                "password": "password123"
            },
            "profile": {
                "title": "Senior Lecturer in Physics",
                "institution": "University of Melbourne",
                "department": "Physics",
                "bio": "Theoretical physicist working on quantum mechanics and quantum computing. Interested in the fundamental nature of reality and its practical applications.",
                "pfp": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
                "location": "Melbourne, Australia",
                "research_interests": "Quantum Mechanics, Quantum Computing, Theoretical Physics, Quantum Information"
            },
            "education": [
                {"degree": "PhD in Physics", "institution": "University of Cambridge", "start_year": 2010, "end_year": 2014},
                {"degree": "Master of Physics", "institution": "University of Oxford", "start_year": 2008, "end_year": 2010}
            ],
            "experience": [
                {"role": "Postdoctoral Researcher", "institution": "CERN", "start_year": 2014, "end_year": 2017},
                {"role": "Research Fellow", "institution": "University of Melbourne", "start_year": 2017, "end_year": 2020},
                {"role": "Senior Lecturer", "institution": "University of Melbourne", "start_year": 2020, "end_year": None}
            ],
            "publications": [
                {"title": "Quantum Algorithms for Optimization Problems", "journal": "Physical Review Letters", "year": 2023, "doi": "10.1103/PhysRevLett.130.120601"},
                {"title": "Entanglement in Quantum Systems", "journal": "Nature Physics", "year": 2022, "doi": "10.1038/s41567-022-01689-5"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/james-wilson-physics"},
                {"platform": "Twitter", "url": "https://twitter.com/james_quantum"}
            ]
        },
        {
            "user": {
                "email": "sarah@example.com",
                "first_name": "Sarah",
                "last_name": "Kim",
                "password": "password123"
            },
            "profile": {
                "title": "Postdoctoral Researcher in Psychology",
                "institution": "University of Sydney",
                "department": "Psychology",
                "bio": "Cognitive psychologist studying human behavior and decision-making. Interested in how people process information and make choices in complex environments.",
                "pfp": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
                "location": "Sydney, Australia",
                "research_interests": "Cognitive Psychology, Decision Making, Behavioral Economics, Human-Computer Interaction"
            },
            "education": [
                {"degree": "PhD in Psychology", "institution": "University of Sydney", "start_year": 2018, "end_year": 2022},
                {"degree": "Master of Psychology", "institution": "University of New South Wales", "start_year": 2016, "end_year": 2018}
            ],
            "experience": [
                {"role": "Research Assistant", "institution": "University of Sydney", "start_year": 2022, "end_year": 2023},
                {"role": "Postdoctoral Researcher", "institution": "University of Sydney", "start_year": 2023, "end_year": None}
            ],
            "publications": [
                {"title": "Cognitive Biases in Digital Decision Making", "journal": "Journal of Experimental Psychology", "year": 2023, "doi": "10.1037/xge0001234"},
                {"title": "Human-AI Collaboration in Complex Tasks", "journal": "Cognitive Science", "year": 2022, "doi": "10.1111/cogs.13123"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/sarah-kim-psychology"},
                {"platform": "ResearchGate", "url": "https://researchgate.net/profile/Sarah-Kim-Psychology"}
            ]
        },
        {
            "user": {
                "email": "michael@example.com",
                "first_name": "Michael",
                "last_name": "Brown",
                "password": "password123"
            },
            "profile": {
                "title": "Professor of Medicine",
                "institution": "University of Queensland",
                "department": "Medicine",
                "bio": "Cardiologist and medical researcher specializing in heart disease prevention and treatment. Leading clinical trials for new cardiovascular therapies.",
                "pfp": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&h=150&fit=crop&crop=face",
                "location": "Brisbane, Australia",
                "research_interests": "Cardiology, Heart Disease, Clinical Trials, Medical Technology"
            },
            "education": [
                {"degree": "MD", "institution": "University of Queensland", "start_year": 2000, "end_year": 2006},
                {"degree": "PhD in Medicine", "institution": "Johns Hopkins University", "start_year": 2006, "end_year": 2010}
            ],
            "experience": [
                {"role": "Resident", "institution": "Royal Brisbane Hospital", "start_year": 2006, "end_year": 2010},
                {"role": "Cardiologist", "institution": "Brisbane Heart Institute", "start_year": 2010, "end_year": 2018},
                {"role": "Professor", "institution": "University of Queensland", "start_year": 2018, "end_year": None}
            ],
            "publications": [
                {"title": "Novel Approaches to Heart Failure Treatment", "journal": "New England Journal of Medicine", "year": 2023, "doi": "10.1056/NEJMoa2304567"},
                {"title": "AI in Cardiac Diagnosis", "journal": "The Lancet", "year": 2022, "doi": "10.1016/S0140-6736(22)01234-5"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/michael-brown-cardiology"},
                {"platform": "ResearchGate", "url": "https://researchgate.net/profile/Michael-Brown-Cardiology"}
            ]
        },
        {
            "user": {
                "email": "emma@example.com",
                "first_name": "Emma",
                "last_name": "Taylor",
                "password": "password123"
            },
            "profile": {
                "title": "Senior Research Fellow in Chemistry",
                "institution": "Monash University",
                "department": "Chemistry",
                "bio": "Materials chemist developing sustainable materials and green chemistry solutions. Focused on creating environmentally friendly alternatives to traditional materials.",
                "pfp": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&h=150&fit=crop&crop=face",
                "location": "Melbourne, Australia",
                "research_interests": "Materials Chemistry, Green Chemistry, Sustainability, Nanotechnology"
            },
            "education": [
                {"degree": "PhD in Chemistry", "institution": "Monash University", "start_year": 2014, "end_year": 2018},
                {"degree": "Master of Chemistry", "institution": "University of Melbourne", "start_year": 2012, "end_year": 2014}
            ],
            "experience": [
                {"role": "Postdoctoral Researcher", "institution": "MIT", "start_year": 2018, "end_year": 2021},
                {"role": "Research Fellow", "institution": "Monash University", "start_year": 2021, "end_year": None}
            ],
            "publications": [
                {"title": "Sustainable Materials for Clean Energy", "journal": "Nature Materials", "year": 2023, "doi": "10.1038/s41563-023-01567-8"},
                {"title": "Green Chemistry in Industrial Applications", "journal": "Science", "year": 2022, "doi": "10.1126/science.abc1234"}
            ],
            "socials": [
                {"platform": "Twitter", "url": "https://twitter.com/emma_chem"},
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/emma-taylor-chemistry"}
            ]
        },
        {
            "user": {
                "email": "alex@example.com",
                "first_name": "Alex",
                "last_name": "Johnson",
                "password": "password123"
            },
            "profile": {
                "title": "Lecturer in Mathematics",
                "institution": "University of Adelaide",
                "department": "Mathematics",
                "bio": "Applied mathematician working on mathematical modeling and data analysis. Interested in using mathematical tools to solve real-world problems in various fields.",
                "pfp": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
                "location": "Adelaide, Australia",
                "research_interests": "Applied Mathematics, Data Analysis, Mathematical Modeling, Statistics"
            },
            "education": [
                {"degree": "PhD in Mathematics", "institution": "University of Adelaide", "start_year": 2016, "end_year": 2020},
                {"degree": "Master of Mathematics", "institution": "University of Sydney", "start_year": 2014, "end_year": 2016}
            ],
            "experience": [
                {"role": "Research Assistant", "institution": "University of Adelaide", "start_year": 2020, "end_year": 2022},
                {"role": "Lecturer", "institution": "University of Adelaide", "start_year": 2022, "end_year": None}
            ],
            "publications": [
                {"title": "Mathematical Models for Disease Spread", "journal": "Mathematical Biosciences", "year": 2023, "doi": "10.1016/j.mbs.2023.108987"},
                {"title": "Statistical Methods in Climate Analysis", "journal": "Journal of Applied Statistics", "year": 2022, "doi": "10.1080/02664763.2022.1234567"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/alex-johnson-mathematics"},
                {"platform": "GitHub", "url": "https://github.com/alex-math"}
            ]
        },
        {
            "user": {
                "email": "lisa@example.com",
                "first_name": "Lisa",
                "last_name": "Wang",
                "password": "password123"
            },
            "profile": {
                "title": "Associate Professor of Engineering",
                "institution": "University of New South Wales",
                "department": "Engineering",
                "bio": "Biomedical engineer developing medical devices and prosthetics. Passionate about using engineering principles to improve healthcare and quality of life for patients.",
                "pfp": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face",
                "location": "Sydney, Australia",
                "research_interests": "Biomedical Engineering, Medical Devices, Prosthetics, Healthcare Technology"
            },
            "education": [
                {"degree": "PhD in Biomedical Engineering", "institution": "Johns Hopkins University", "start_year": 2010, "end_year": 2014},
                {"degree": "Master of Engineering", "institution": "University of New South Wales", "start_year": 2008, "end_year": 2010}
            ],
            "experience": [
                {"role": "Research Engineer", "institution": "Medtronic", "start_year": 2014, "end_year": 2018},
                {"role": "Assistant Professor", "institution": "University of New South Wales", "start_year": 2018, "end_year": 2023},
                {"role": "Associate Professor", "institution": "University of New South Wales", "start_year": 2023, "end_year": None}
            ],
            "publications": [
                {"title": "Advanced Prosthetic Limbs with Neural Control", "journal": "Nature Biomedical Engineering", "year": 2023, "doi": "10.1038/s41551-023-01089-2"},
                {"title": "Wearable Health Monitoring Devices", "journal": "IEEE Transactions on Biomedical Engineering", "year": 2022, "doi": "10.1109/TBME.2022.1234567"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/lisa-wang-engineering"},
                {"platform": "Twitter", "url": "https://twitter.com/lisa_bioeng"}
            ]
        },
        {
            "user": {
                "email": "robert@example.com",
                "first_name": "Robert",
                "last_name": "Anderson",
                "password": "password123"
            },
            "profile": {
                "title": "Research Professor of Economics",
                "institution": "Australian National University",
                "department": "Economics",
                "bio": "Behavioral economist studying decision-making and market behavior. Interested in how psychological factors influence economic choices and policy outcomes.",
                "pfp": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
                "location": "Canberra, Australia",
                "research_interests": "Behavioral Economics, Decision Making, Market Psychology, Economic Policy"
            },
            "education": [
                {"degree": "PhD in Economics", "institution": "University of Chicago", "start_year": 2008, "end_year": 2012},
                {"degree": "Master of Economics", "institution": "London School of Economics", "start_year": 2006, "end_year": 2008}
            ],
            "experience": [
                {"role": "Research Fellow", "institution": "Federal Reserve Bank", "start_year": 2012, "end_year": 2016},
                {"role": "Associate Professor", "institution": "Australian National University", "start_year": 2016, "end_year": 2021},
                {"role": "Research Professor", "institution": "Australian National University", "start_year": 2021, "end_year": None}
            ],
            "publications": [
                {"title": "Behavioral Insights in Public Policy", "journal": "American Economic Review", "year": 2023, "doi": "10.1257/aer.20231234"},
                {"title": "Cognitive Biases in Financial Decision Making", "journal": "Journal of Economic Literature", "year": 2022, "doi": "10.1257/jel.20221234"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/robert-anderson-economics"},
                {"platform": "ResearchGate", "url": "https://researchgate.net/profile/Robert-Anderson-Economics"}
            ]
        },
        {
            "user": {
                "email": "sophie@example.com",
                "first_name": "Sophie",
                "last_name": "White",
                "password": "password123"
            },
            "profile": {
                "title": "Senior Lecturer in Linguistics",
                "institution": "Macquarie University",
                "department": "Linguistics",
                "bio": "Computational linguist working on natural language processing and language technology. Interested in how computers can understand and generate human language.",
                "pfp": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=150&h=150&fit=crop&crop=face",
                "location": "Sydney, Australia",
                "research_interests": "Computational Linguistics, Natural Language Processing, Language Technology, Machine Translation"
            },
            "education": [
                {"degree": "PhD in Linguistics", "institution": "Stanford University", "start_year": 2015, "end_year": 2019},
                {"degree": "Master of Linguistics", "institution": "Macquarie University", "start_year": 2013, "end_year": 2015}
            ],
            "experience": [
                {"role": "Research Scientist", "institution": "Google", "start_year": 2019, "end_year": 2022},
                {"role": "Senior Lecturer", "institution": "Macquarie University", "start_year": 2022, "end_year": None}
            ],
            "publications": [
                {"title": "Multilingual Language Models for Low-Resource Languages", "journal": "Computational Linguistics", "year": 2023, "doi": "10.1162/coli_a_00456"},
                {"title": "Cross-Linguistic Analysis of Sentiment", "journal": "Language Resources and Evaluation", "year": 2022, "doi": "10.1007/s10579-022-09578-9"}
            ],
            "socials": [
                {"platform": "GitHub", "url": "https://github.com/sophie-linguistics"},
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/sophie-white-linguistics"}
            ]
        },
        {
            "user": {
                "email": "anna@example.com",
                "first_name": "Anna",
                "last_name": "Petrov",
                "password": "password123"
            },
            "profile": {
                "title": "Research Fellow in Neuroscience",
                "institution": "University of Western Australia",
                "department": "Neuroscience",
                "bio": "Neuroscientist studying brain plasticity and learning mechanisms. Focused on understanding how the brain adapts and recovers from injury.",
                "pfp": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&h=150&fit=crop&crop=face",
                "location": "Perth, Australia",
                "research_interests": "Neuroscience, Brain Plasticity, Learning, Neurorehabilitation, Cognitive Science"
            },
            "education": [
                {"degree": "PhD in Neuroscience", "institution": "University of Western Australia", "start_year": 2015, "end_year": 2019},
                {"degree": "Master of Science", "institution": "University of Melbourne", "start_year": 2013, "end_year": 2015}
            ],
            "experience": [
                {"role": "Postdoctoral Researcher", "institution": "UCLA", "start_year": 2019, "end_year": 2022},
                {"role": "Research Fellow", "institution": "University of Western Australia", "start_year": 2022, "end_year": None}
            ],
            "publications": [
                {"title": "Neural Mechanisms of Learning and Memory", "journal": "Nature Neuroscience", "year": 2023, "doi": "10.1038/s41593-023-01345-6"},
                {"title": "Brain Plasticity in Stroke Recovery", "journal": "Journal of Neuroscience", "year": 2022, "doi": "10.1523/JNEUROSCI.1234-22.2022"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/anna-petrov-neuroscience"},
                {"platform": "ResearchGate", "url": "https://researchgate.net/profile/Anna-Petrov-Neuroscience"}
            ]
        },
        {
            "user": {
                "email": "tom@example.com",
                "first_name": "Tom",
                "last_name": "Anderson",
                "password": "password123"
            },
            "profile": {
                "title": "Senior Lecturer in Data Science",
                "institution": "Curtin University",
                "department": "Data Science",
                "bio": "Data scientist and statistician working on machine learning applications in healthcare and social sciences. Passionate about making data science accessible and ethical.",
                "pfp": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
                "location": "Perth, Australia",
                "research_interests": "Data Science, Machine Learning, Healthcare Analytics, Statistical Modeling, Big Data"
            },
            "education": [
                {"degree": "PhD in Statistics", "institution": "University of California, Berkeley", "start_year": 2010, "end_year": 2014},
                {"degree": "Master of Statistics", "institution": "University of Sydney", "start_year": 2008, "end_year": 2010}
            ],
            "experience": [
                {"role": "Data Scientist", "institution": "Microsoft Research", "start_year": 2014, "end_year": 2018},
                {"role": "Senior Lecturer", "institution": "Curtin University", "start_year": 2018, "end_year": None}
            ],
            "publications": [
                {"title": "Machine Learning in Healthcare: Opportunities and Challenges", "journal": "Nature Machine Intelligence", "year": 2023, "doi": "10.1038/s42256-023-00678-0"},
                {"title": "Statistical Methods for Big Data Analysis", "journal": "Journal of the American Statistical Association", "year": 2022, "doi": "10.1080/01621459.2022.1234567"}
            ],
            "socials": [
                {"platform": "GitHub", "url": "https://github.com/tom-anderson-datascience"},
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/tom-anderson-datascience"}
            ]
        },
        {
            "user": {
                "email": "yuki@example.com",
                "first_name": "Yuki",
                "last_name": "Tanaka",
                "password": "password123"
            },
            "profile": {
                "title": "Associate Professor of Robotics",
                "institution": "University of Technology Sydney",
                "department": "Robotics Engineering",
                "bio": "Robotics engineer developing autonomous systems and human-robot interaction. Working on next-generation robots for healthcare and manufacturing applications.",
                "pfp": "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
                "location": "Sydney, Australia",
                "research_interests": "Robotics, Autonomous Systems, Human-Robot Interaction, Artificial Intelligence, Machine Learning"
            },
            "education": [
                {"degree": "PhD in Robotics", "institution": "Tokyo Institute of Technology", "start_year": 2012, "end_year": 2016},
                {"degree": "Master of Engineering", "institution": "University of Tokyo", "start_year": 2010, "end_year": 2012}
            ],
            "experience": [
                {"role": "Research Engineer", "institution": "Honda Research Institute", "start_year": 2016, "end_year": 2020},
                {"role": "Assistant Professor", "institution": "University of Technology Sydney", "start_year": 2020, "end_year": 2023},
                {"role": "Associate Professor", "institution": "University of Technology Sydney", "start_year": 2023, "end_year": None}
            ],
            "publications": [
                {"title": "Autonomous Navigation in Dynamic Environments", "journal": "IEEE Transactions on Robotics", "year": 2023, "doi": "10.1109/TRO.2023.1234567"},
                {"title": "Human-Robot Collaboration in Manufacturing", "journal": "Science Robotics", "year": 2022, "doi": "10.1126/scirobotics.abc1234"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/yuki-tanaka-robotics"},
                {"platform": "GitHub", "url": "https://github.com/yuki-robotics"}
            ]
        },
        {
            "user": {
                "email": "priya@example.com",
                "first_name": "Priya",
                "last_name": "Sharma",
                "password": "password123"
            },
            "profile": {
                "title": "Professor of Public Health",
                "institution": "University of Melbourne",
                "department": "Public Health",
                "bio": "Public health researcher focusing on global health equity and infectious disease prevention. Leading studies on health disparities and community-based interventions.",
                "pfp": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face",
                "location": "Melbourne, Australia",
                "research_interests": "Public Health, Global Health, Infectious Diseases, Health Equity, Epidemiology"
            },
            "education": [
                {"degree": "PhD in Public Health", "institution": "Johns Hopkins University", "start_year": 2008, "end_year": 2012},
                {"degree": "Master of Public Health", "institution": "University of Melbourne", "start_year": 2006, "end_year": 2008}
            ],
            "experience": [
                {"role": "Research Fellow", "institution": "World Health Organization", "start_year": 2012, "end_year": 2016},
                {"role": "Associate Professor", "institution": "University of Melbourne", "start_year": 2016, "end_year": 2021},
                {"role": "Professor", "institution": "University of Melbourne", "start_year": 2021, "end_year": None}
            ],
            "publications": [
                {"title": "Global Health Equity in the Post-Pandemic World", "journal": "The Lancet", "year": 2023, "doi": "10.1016/S0140-6736(23)01234-5"},
                {"title": "Community-Based Interventions for Disease Prevention", "journal": "American Journal of Public Health", "year": 2022, "doi": "10.2105/AJPH.2022.123456"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/priya-sharma-publichealth"},
                {"platform": "Twitter", "url": "https://twitter.com/priya_publichealth"}
            ]
        },
        {
            "user": {
                "email": "marcus@example.com",
                "first_name": "Marcus",
                "last_name": "Johnson",
                "password": "password123"
            },
            "profile": {
                "title": "Senior Research Fellow in Climate Science",
                "institution": "Australian National University",
                "department": "Climate Science",
                "bio": "Climate scientist studying atmospheric dynamics and climate change impacts. Using advanced modeling techniques to predict future climate scenarios and inform policy decisions.",
                "pfp": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
                "location": "Canberra, Australia",
                "research_interests": "Climate Science, Atmospheric Physics, Climate Modeling, Environmental Policy, Sustainability"
            },
            "education": [
                {"degree": "PhD in Atmospheric Sciences", "institution": "MIT", "start_year": 2010, "end_year": 2014},
                {"degree": "Master of Science", "institution": "University of California, Berkeley", "start_year": 2008, "end_year": 2010}
            ],
            "experience": [
                {"role": "Postdoctoral Researcher", "institution": "NASA Goddard Institute", "start_year": 2014, "end_year": 2017},
                {"role": "Research Scientist", "institution": "CSIRO", "start_year": 2017, "end_year": 2020},
                {"role": "Senior Research Fellow", "institution": "Australian National University", "start_year": 2020, "end_year": None}
            ],
            "publications": [
                {"title": "Climate Change Projections for the 21st Century", "journal": "Nature Climate Change", "year": 2023, "doi": "10.1038/s41558-023-01678-9"},
                {"title": "Atmospheric Dynamics and Extreme Weather Events", "journal": "Science", "year": 2022, "doi": "10.1126/science.abc1234"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/marcus-johnson-climate"},
                {"platform": "ResearchGate", "url": "https://researchgate.net/profile/Marcus-Johnson-Climate"}
            ]
        },
        {
            "user": {
                "email": "zara@example.com",
                "first_name": "Zara",
                "last_name": "Ahmed",
                "password": "password123"
            },
            "profile": {
                "title": "Lecturer in Digital Humanities",
                "institution": "University of Sydney",
                "department": "Digital Humanities",
                "bio": "Digital humanities scholar exploring the intersection of technology and culture. Using computational methods to analyze historical texts and cultural artifacts.",
                "pfp": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
                "location": "Sydney, Australia",
                "research_interests": "Digital Humanities, Cultural Studies, Text Analysis, Digital Archives, Computational Linguistics"
            },
            "education": [
                {"degree": "PhD in Digital Humanities", "institution": "University of Sydney", "start_year": 2016, "end_year": 2020},
                {"degree": "Master of Arts", "institution": "University of Oxford", "start_year": 2014, "end_year": 2016}
            ],
            "experience": [
                {"role": "Research Assistant", "institution": "British Library", "start_year": 2020, "end_year": 2022},
                {"role": "Lecturer", "institution": "University of Sydney", "start_year": 2022, "end_year": None}
            ],
            "publications": [
                {"title": "Computational Analysis of Historical Texts", "journal": "Digital Humanities Quarterly", "year": 2023, "doi": "10.1000/dhq.2023.123"},
                {"title": "Digital Archives and Cultural Preservation", "journal": "Journal of Digital Humanities", "year": 2022, "doi": "10.1000/jdh.2022.456"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/zara-ahmed-digitalhumanities"},
                {"platform": "Twitter", "url": "https://twitter.com/zara_digitalhum"}
            ]
        },
        {
            "user": {
                "email": "kevin@example.com",
                "first_name": "Kevin",
                "last_name": "O'Connor",
                "password": "password123"
            },
            "profile": {
                "title": "Research Professor of Marine Biology",
                "institution": "James Cook University",
                "department": "Marine Biology",
                "bio": "Marine biologist studying coral reef ecosystems and ocean conservation. Leading research on climate change impacts on marine biodiversity and developing conservation strategies.",
                "pfp": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&h=150&fit=crop&crop=face",
                "location": "Townsville, Australia",
                "research_interests": "Marine Biology, Coral Reefs, Ocean Conservation, Climate Change, Marine Biodiversity"
            },
            "education": [
                {"degree": "PhD in Marine Biology", "institution": "James Cook University", "start_year": 2005, "end_year": 2009},
                {"degree": "Master of Science", "institution": "University of Queensland", "start_year": 2003, "end_year": 2005}
            ],
            "experience": [
                {"role": "Postdoctoral Researcher", "institution": "Scripps Institution of Oceanography", "start_year": 2009, "end_year": 2012},
                {"role": "Research Fellow", "institution": "James Cook University", "start_year": 2012, "end_year": 2018},
                {"role": "Research Professor", "institution": "James Cook University", "start_year": 2018, "end_year": None}
            ],
            "publications": [
                {"title": "Coral Reef Resilience in a Changing Climate", "journal": "Nature", "year": 2023, "doi": "10.1038/s41586-023-06234-5"},
                {"title": "Marine Conservation Strategies for the Great Barrier Reef", "journal": "Science", "year": 2022, "doi": "10.1126/science.abc1234"}
            ],
            "socials": [
                {"platform": "LinkedIn", "url": "https://linkedin.com/in/kevin-oconnor-marinebiology"},
                {"platform": "ResearchGate", "url": "https://researchgate.net/profile/Kevin-OConnor-MarineBiology"}
            ]
        }
    ]

    # Create all users and their profiles
    for user_data in users_data:
        # Create user
        user = User(
            email=user_data["user"]["email"],
            first_name=user_data["user"]["first_name"],
            last_name=user_data["user"]["last_name"]
        )
        user.set_password(user_data["user"]["password"])
        db.session.add(user)
        db.session.commit()

        # Create profile
        profile = Profile(
            user_id=user.id,
            title=user_data["profile"]["title"],
            institution=user_data["profile"]["institution"],
            department=user_data["profile"]["department"],
            bio=user_data["profile"]["bio"],
            pfp=user_data["profile"]["pfp"],
            location=user_data["profile"]["location"],
            research_interests=user_data["profile"]["research_interests"]
        )
        db.session.add(profile)
        db.session.commit()

        # Create education records
        for edu_data in user_data["education"]:
            edu = Education(
                pid=profile.pid,
                degree=edu_data["degree"],
                institution=edu_data["institution"],
                start_year=edu_data["start_year"],
                end_year=edu_data["end_year"]
            )
            db.session.add(edu)

        # Create experience records
        for exp_data in user_data["experience"]:
            exp = Experience(
                pid=profile.pid,
                role=exp_data["role"],
                institution=exp_data["institution"],
                start_year=exp_data["start_year"],
                end_year=exp_data["end_year"]
            )
            db.session.add(exp)

        # Create publications
        for pub_data in user_data["publications"]:
            pub = Publication(
                pid=profile.pid,
                title=pub_data["title"],
                journal=pub_data["journal"],
                year=pub_data["year"],
                doi=pub_data["doi"],
                url=f"https://doi.org/{pub_data['doi']}"
            )
            db.session.add(pub)

        # Create social links
        for social_data in user_data["socials"]:
            social = Social(
                pid=profile.pid,
                platform=social_data["platform"],
                url=social_data["url"]
            )
            db.session.add(social)

    db.session.commit()
    print(f"Sample data loaded with Alice (original) + {len(users_data)} additional users = {len(users_data) + 1} total users.")