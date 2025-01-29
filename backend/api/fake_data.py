from faker import Faker
from users.models import CustomUser
from jobs.models import Job, JobCategory
from sqlalchemy.exc import IntegrityError
import math
import random

fake = Faker()


class FakeUtil:

    def get_group_amount(self, amount: int) -> int:
        return math.ceil(amount / 2)


class FakeUsers(FakeUtil):
    """Generate fake data for modelss in Users app"""

    def users(self, amount=100):
        group_amount = self.get_group_amount(amount)
        for _ in range(group_amount):
            CustomUser.objects.create(
                password=fake.password(),
                username=fake.user_name(),
                first_name=fake.first_name(),
                email=fake.email(),
                category="Individual",
                location=fake.address(),
                phone_number=fake.phone_number(),
            ).save()
            print(f"> Users faked [{_+1}/{amount}]", end="\r")

        for _ in range(group_amount):
            name = fake.company()
            CustomUser.objects.create(
                password=fake.password(),
                username=name,
                first_name=name,
                email=fake.company_email(),
                category="Organization",
                location=fake.address(),
                phone_number=fake.phone_number(),
            ).save()
            print(f"> Users faked [{_+1+group_amount}/{amount}]", end="\r")


class FakeJob(FakeUtil):
    """Generate fake data for models in Jobs app"""

    job_categories = [
        "Software Engineer",
        "Data Scientist",
        "Product Manager",
        "UX Designer",
        "DevOps Engineer",
        "Solutions Architect",
        "Business Analyst",
        "Marketing Specialist",
        "HR Generalist",
        "Financial Analyst",
        "Graphic Designer",
        "Content Writer",
        "Sales Representative",
        "Customer Service Representative",
        "Operations Manager",
        "Network Administrator",
        "Project Manager",
        "Accountant",
        "Digital Marketing Specialist",
        "IT Support Specialist",
        "Web Developer",
        "Database Administrator",
        "Cybersecurity Specialist",
        "Cloud Computing Professional",
        "Artificial Intelligence Engineer",
        "Machine Learning Engineer",
        "Blockchain Developer",
        "Full Stack Developer",
        "Front End Developer",
        "Back End Developer",
        "Quality Assurance Engineer",
        "Data Analyst",
        "Business Intelligence Developer",
        "Digital Product Manager",
        "User Experience Researcher",
        "Product Designer",
        "Technical Writer",
        "Recruiter",
        "Supply Chain Manager",
        "Logistics Coordinator",
        "Event Planner",
        "Interior Designer",
        "Fashion Designer",
        "Graphic Illustrator",
        "Video Editor",
        "Sound Engineer",
        "Game Developer",
        "UX/UI Designer",
    ]

    def category(self, amount=50):
        """Fake JobCategory"""
        for count, category in enumerate(self.job_categories, start=1):
            try:
                JobCategory.objects.create(
                    name=category,
                    description=fake.text(random.randint(60, 100)),
                ).save()
                print(f"> Categories faked [{count}/{amount}]", end="\r")
                if count == amount:
                    break
            except IntegrityError:
                pass

    def job(self, amount=100):
        """Fake Job"""
        group_amount = self.get_group_amount(amount)
        categories = JobCategory.objects.all()
        companies = CustomUser.objects.filter(category="Organization").all()
        for _ in range(group_amount):
            Job.objects.create(
                company=random.choice(companies),
                category=random.choice(categories),
                title=fake.sentence(),
                type=random.choice(["Full-time", "Internship"]),
                minimum_salary=random.randint(20000, 70000),
                maximum_salary=random.randint(70001, 150000),
                description=fake.paragraph(random.randint(1, 4)),
            ).save()
            print(f"> Jobs faked [{_+1}/{amount}]", end="\r")
