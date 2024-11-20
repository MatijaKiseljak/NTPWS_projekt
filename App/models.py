from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class PredavacIzborModel(models.Model):
    EDUCATION_CHOICES = [
        ('diplomski_studij', 'Sveučilišni diplomski ili stručni diplomski studij'),
        ('neki_drugi', 'Neki drugi studij'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES, help_text="Navedite završen studij")
    diploma_document = models.FileField(upload_to='Diplome/', null=True, blank=True, help_text="Upload your diploma")
    teaching_hours = models.PositiveIntegerField(help_text="Broj održanih norma sati u sustavu visokog obrazovanja", null=True, blank=True)
    crosbi_profile_link = models.URLField(max_length=200, null=True, blank=True, help_text="Link to your updated Crosbi profile")
    number_of_published_papers = models.PositiveIntegerField(help_text="Broj objavljenih stručnih ili znanstvenih radova", default=0)
    papers_documents = models.FileField(upload_to='Radovi/', null=True, blank=True, help_text="Upload your papers (in ZIP format if multiple)")
    patent_document = models.FileField(upload_to='Patenti/', null=True, blank=True, help_text="Upload document of patent proof")

    def __str__(self):
        return f"{self.user.username} - Predavač izbor"
    
class PredavacReizborModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    is_elected_lecturer = models.BooleanField(default=False, help_text="Jeste li bili izabrani na nastavno mjesto predavača")
    teaching_hours = models.PositiveIntegerField(help_text="Broj održanih norma sati nastave", null=True, blank=True)
    published_works_count = models.PositiveIntegerField(help_text="Broj objavljenih stručnih, znanstvenih ili umjetničkih radova", default=0)
    papers_documents = models.FileField(upload_to='Radovi/', null=True, blank=True, help_text="Upload your papers (in ZIP format if multiple)")

    project_leadership_experience = models.BooleanField(default=False, help_text="Imate li iskustvo vođenja ili suvoditeljstva na projektima?")

    def __str__(self):
        return f"{self.user.username} - Predavač reizbor"
    

class VisiPredavacIzborModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    diploma_document = models.FileField(upload_to='Diplome/', null=True, blank=True, help_text="Upload your diploma")
    teaching_hours = models.PositiveIntegerField(help_text="Broj održanih norma sati u sustavu visokog obrazovanja", null=True, blank=True)
    crosbi_profile_link = models.URLField(max_length=200, null=True, blank=True, help_text="Link to your updated Crosbi profile")
    teaching_material = models.FileField(upload_to='Nastavni materijali/', null=True, blank=True, help_text="Upload your teaching material")
    mentoring = models.FileField(upload_to='Mentorstva/', null=True, blank=True, help_text="Upload your final assigment's with students in ZIP format")
    gatherings = models.BooleanField(default=False, help_text="Jeste li sudjelovali na domaćim ili međunarodnim skupovima?")
    reviewed_scientific_papers = models.FileField(upload_to='Recenzirani radovi/', null=True, blank=True, help_text="Upload scientific papers that you reviewed in ZIP format")
    
    def __str__(self):
        return f"{self.user.username} - Viši predavač izbor"
    
class VisiPredavacReizborModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    teaching_hours = models.PositiveIntegerField(help_text="Broj održanih norma sati nastave", null=True, blank=True)
    crosbi_profile_link = models.URLField(max_length=200, null=True, blank=True, help_text="Link to your updated Crosbi profile")
    scientific_paper_high_level = models.FileField(upload_to='Znanstveni radovi/', null=True, blank=True, help_text="Upload your scientific papers (in ZIP format if multiple)")
    doctorate_or_alternative = models.FileField(upload_to='Diplome/', null=True, blank=True, help_text="Upload your doctorate diploma or alternative scientific contribution")
    scientific_papers = models.FileField(upload_to='Znanstveni radovi/', null=True, blank=True, help_text="Upload at least three scientific papers that you wrote in ZIP format")
    project_participation = models.FileField(upload_to='Znanstveni radovi/', null=True, blank=True, help_text="Upload projects that you participated in")

    def __str__(self):
        return f"{self.user.username} - Viši predavač reizbor"
    
class  ProfesorStrucnogStudijaIzborModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    doctorate_or_alternative = models.FileField(upload_to='Diplome/', null=True, blank=True, help_text="Upload your doctorate diploma or alternative scientific contribution")
    teaching = models.PositiveIntegerField(help_text="Broj održanih norma sati nastaveu prethodnom izbornom razdoblju", null=True, blank=True)


    reviewed_teaching_material = models.BooleanField(default=False, help_text="Has published reviewed teaching material for the course.")
    mentorship_count = models.PositiveIntegerField(default=0, help_text="Number of mentored final and/or graduate theses.")
    coauthored_papers_with_students = models.PositiveIntegerField(default=0, help_text="Number of co-authored papers with students.")
    presented_papers_count = models.PositiveIntegerField(default=0, help_text="Number of presented papers at conferences.")
    international_papers_count = models.PositiveIntegerField(default=0, help_text="Number of international conference presentations.")
    participated_in_international_mobility = models.BooleanField(default=False, help_text="Has participated in international mobility or professional training.")
    led_international_project = models.BooleanField(default=False, help_text="Has led an international project or significant documented contribution in relevant fields.")
    received_international_award = models.BooleanField(default=False, help_text="Has received an international or notable domestic award for educational, scientific, or artistic contribution.")
    google_scholar_citations = models.PositiveIntegerField(default=0, help_text="Number of new confirmed Google Scholar citations.")
    exhibitions_count = models.PositiveIntegerField(default=0, help_text="Number of organized artistic exhibitions.")
    reviewed_academic_manuals = models.PositiveIntegerField(default=0, help_text="Number of reviewed academic manuals or textbooks.")
    attended_professional_workshops = models.PositiveIntegerField(default=0, help_text="Number of professional workshops attended in the relevant scientific field.")

    def __str__(self):
        return f"{self.user.username} - Profesor stručnog studija izbor"

class  ProfesorStrucnogStudijaReizborModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    has_reviewed_teaching_material = models.BooleanField(default=False, help_text="Has published reviewed teaching material for the course.")
    mentorship_theses_count = models.PositiveIntegerField(default=0, help_text="Number of final and/or graduate theses mentored (min. 7).")
    coauthored_papers_with_students_count = models.PositiveIntegerField(default=0, help_text="Number of co-authored papers with students (min. 3).")
    presented_papers_count = models.PositiveIntegerField(default=0, help_text="Total number of presented papers at conferences (min. 4).")
    international_papers_count = models.PositiveIntegerField(default=0, help_text="Number of international conference presentations (min. 2).")
    participated_in_international_mobility = models.BooleanField(default=False, help_text="Has participated in international mobility or professional training.")
    led_international_project = models.BooleanField(default=False, help_text="Has led an international project or documented significant professional contribution in the field.")
    received_award = models.BooleanField(default=False, help_text="Has received an international or significant domestic award.")
    google_scholar_citations = models.PositiveIntegerField(default=0, help_text="New confirmed Google Scholar citations (min. 20).")
    exhibitions_count = models.PositiveIntegerField(default=0, help_text="Number of organized artistic exhibitions (min. 5).")
    reviewed_academic_manuals = models.PositiveIntegerField(default=0, help_text="Number of reviewed academic manuals or involvement in program organization (min. 1).")
    attended_professional_workshops = models.PositiveIntegerField(default=0, help_text="Number of professional workshops attended in the relevant field (min. 5).")

    def __str__(self):
        return f"{self.user.username} - Profesor stručnog studija reizbor" 

class ProfesorStrucnogStudijaTrajniModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    has_previous_professor_position = models.BooleanField(default=False, help_text="Already held the position of professor in the previous term.")
    teaching_hours_last_term = models.PositiveIntegerField(default=0, help_text="Number of teaching hours completed in the previous term (min. 240).")
    

    academic_papers_count = models.PositiveIntegerField(default=0, help_text="Number of published academic papers or projects (min. 3).")
    patents_count = models.PositiveIntegerField(default=0, help_text="Number of recognized patents.")
    

    translations_count = models.PositiveIntegerField(default=0, help_text="For philology: Number of translated works.")
    sports_team_management_count = models.PositiveIntegerField(default=0, help_text="For kinesiology: Number of student teams managed (min. 3).")


    has_reviewed_teaching_material = models.BooleanField(default=False, help_text="Has published reviewed teaching material.")
    mentorship_theses_count = models.PositiveIntegerField(default=0, help_text="Number of mentored final or graduate theses (min. 7).")
    coauthored_papers_with_students_count = models.PositiveIntegerField(default=0, help_text="Number of co-authored papers with students (min. 3).")
    presented_papers_count = models.PositiveIntegerField(default=0, help_text="Total number of papers presented at conferences (min. 4).")
    international_papers_count = models.PositiveIntegerField(default=0, help_text="Number of international conference presentations (min. 2).")
    participated_in_international_mobility = models.BooleanField(default=False, help_text="Participated in international mobility or professional training.")
    led_international_project = models.BooleanField(default=False, help_text="Led an international project or contributed significantly to one.")
    highest_level_works_count = models.PositiveIntegerField(default=0, help_text="Number of high-level works or projects (min. 2).")
    received_award = models.BooleanField(default=False, help_text="Received international or significant domestic award.")
    google_scholar_citations = models.PositiveIntegerField(default=0, help_text="New confirmed citations on Google Scholar (min. 20).")
    exhibitions_count = models.PositiveIntegerField(default=0, help_text="Number of artistic exhibitions attended or organized (min. 5).")
    reviewed_academic_manuals_count = models.PositiveIntegerField(default=0, help_text="Reviewed academic manuals or participated in curriculum innovation (min. 1).")
    
    def __str__(self):
        return f"{self.user.username} - Profesor stručnog studija u trajnom izboru" 
    
class Prijava(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    prijava_content = GenericForeignKey('content_type', 'object_id')

    prijava_tip = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.prijava_tip} - {self.user.username}" 
    