from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import (
    PredavacIzborModel,PredavacReizborModel, 
    VisiPredavacIzborModel, VisiPredavacReizborModel, 
    ProfesorStrucnogStudijaIzborModel, ProfesorStrucnogStudijaReizborModel, ProfesorStrucnogStudijaTrajniModel,
    )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_superuser=False
        )
        return user
    
    
class CMSRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"password2": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            is_superuser=True
        )
        return user


class PredavacIzborSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredavacIzborModel
        fields = [
            'created_at',
            'education_level', 
            'diploma_document',
            'teaching_hours', 
            'crosbi_profile_link',
            'number_of_published_papers',
            'papers_documents',
            'patent_document'
        ]

    def validate_education_level(self, value):
        if not value:
            raise serializers.ValidationError("Razina obrazovanja je obavezna.")
        return value

    def validate_diploma_document(self, value):
        if not value:
            raise serializers.ValidationError("Diploma je obavezna. Molimo da priložite svoju diplomu.")
        return value

    def validate_teaching_hours(self, value):
        if value is None:
            raise serializers.ValidationError("Broj održanih sati nastave je obavezan.")
        elif value < 0:
            raise serializers.ValidationError("Broj održanih sati nastave ne može biti negativan.")
        return value

    def validate_crosbi_profile_link(self, value):
        if not value:
            raise serializers.ValidationError("Link na Crosbi profil je obavezan.")
        if not value.startswith("http"):
            raise serializers.ValidationError("Molimo unesite ispravan URL za svoj Crosbi profil.")
        return value

    def validate_number_of_published_papers(self, value):
        if value is None:
            raise serializers.ValidationError("Broj objavljenih radova je obavezan.")
        elif value < 2:
            raise serializers.ValidationError("Morate imati najmanje 2 objavljena rada.")
        return value

    def validate_papers_documents(self, value):
        if not value:
            raise serializers.ValidationError("Molimo priložite svoje objavljene radove.")
        return value

    def validate_patent_document(self, value):
        if not value:
            raise serializers.ValidationError("Dokument o patentu je obavezan. Molimo da priložite dokument koji potvrđuje vaš patent.")
        return value
    
class PredavacReizborSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredavacReizborModel
        fields = [
            'created_at',
            'is_elected_lecturer', 
            'teaching_hours', 
            'published_works_count',
            'papers_documents',
            'project_leadership_experience',
        ]
    def validate_elected_lecturer(self, value):
        if not value:
            raise serializers.ValidationError("Obavezno unesite jeste li bili izabrani na nastavno mjesto predavača")
        return value
    
    def validate_teaching_hours(self, value):
        if value is None:
            raise serializers.ValidationError("Broj održanih sati nastave je obavezan.")
        elif value < 0:
            raise serializers.ValidationError("Broj održanih sati nastave ne može biti negativan.")
        return value
    
    def validate_published_works(self, value):
        if not value:
            raise serializers.ValidationError("Obavezno unesite broj objavljenih stručnih, znanstvenih ili umjetničkih radova")
        return value
    
    def validate_papers_documents(self, value):
        if not value:
            raise serializers.ValidationError("Molimo priložite svoje objavljene radove.")
        return value
    
    def validate_project_leadership(self, value):
        if not value:
            raise serializers.ValidationError("Obavezno uneiste Imate li iskustvo vođenja ili suvoditeljstva na projektima?")
        return value
    
class VisiPredavacIzborSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisiPredavacIzborModel
        fields = [
            'created_at',
            'diploma_document',
            'teaching_hours', 
            'crosbi_profile_link',
            'teaching_material',
            'mentoring',
            'gatherings',
            'reviewed_scientific_papers',
        ]
    def validate_education_level(self, value):
        if not value:
            raise serializers.ValidationError("Razina obrazovanja je obavezna.")
        return value
    
    def validate_diploma_document(self, value):
        if not value:
            raise serializers.ValidationError("Diploma je obavezna. Molimo da priložite svoju diplomu.")
        return value 
    
    def validate_teaching_hours(self, value):
        if value is None:
            raise serializers.ValidationError("Broj održanih sati nastave je obavezan.")
        elif value < 0:
            raise serializers.ValidationError("Broj održanih sati nastave ne može biti negativan.")
        return value
    
    def validate_crosbi_profile_link(self, value):
        if not value:
            raise serializers.ValidationError("Link na Crosbi profil je obavezan.")
        if not value.startswith("http"):
            raise serializers.ValidationError("Molimo unesite ispravan URL za svoj Crosbi profil.")
        return value   
    
    def validate_teaching_material(self, value):
        if not value:
            raise serializers.ValidationError("Obavezno priložite Vaš nastavnički materijal.")
        return value
    
    def validate_mentoring(self, value):
        if not value:
            raise serializers.ValidationError("Obavezno priložite Vaša mentorstva.")
        return value
    
    def validate_gatherings(self, value):
        if not value:
            raise serializers.ValidationError("Molimo da unesete jeste li sudjelovali na domaćim ili međunarodnim skupovima.")
        return value 
    
    def validate_reviewed_scientific_papers(self, value):
        if not value:
            raise serializers.ValidationError("Molimo da unesete Vaše recenzirane radove.")
        return value 

class VisiPredavacReizborSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisiPredavacReizborModel
        fields = [
            'created_at',
            'teaching_hours',
            'crosbi_profile_link',
            'scientific_paper_high_level',
            'doctorate_or_alternative',
            'scientific_papers',
            'project_participation'
        ]


class ProfesorStrucnogStudijaIzborSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorStrucnogStudijaIzborModel
        fields = [
            'created_at',
            'doctorate_or_alternative',
            'teaching',
            'reviewed_teaching_material',
            'mentorship_count',
            'coauthored_papers_with_students',
            'presented_papers_count',
            'international_papers_count',
            'participated_in_international_mobility',
            'led_international_project',
            'received_international_award',
            'google_scholar_citations',
            'exhibitions_count',
            'reviewed_academic_manuals',
            'attended_professional_workshops'
        ]


class ProfesorStrucnogStudijaReizborSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorStrucnogStudijaReizborModel
        fields = [
            'created_at',
            'has_reviewed_teaching_material',
            'mentorship_theses_count',
            'coauthored_papers_with_students_count',
            'presented_papers_count',
            'international_papers_count',
            'participated_in_international_mobility',
            'led_international_project',
            'received_award',
            'google_scholar_citations',
            'exhibitions_count',
            'reviewed_academic_manuals',
            'attended_professional_workshops'
        ]


class ProfesorStrucnogStudijaTrajniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorStrucnogStudijaTrajniModel
        fields = [
            'created_at',
            'has_previous_professor_position',
            'teaching_hours_last_term',
            'academic_papers_count',
            'patents_count',
            'translations_count',
            'sports_team_management_count',
            'has_reviewed_teaching_material',
            'mentorship_theses_count',
            'coauthored_papers_with_students_count',
            'presented_papers_count',
            'international_papers_count',
            'participated_in_international_mobility',
            'led_international_project',
            'highest_level_works_count',
            'received_award',
            'google_scholar_citations',
            'exhibitions_count',
            'reviewed_academic_manuals_count'
        ]

    def validate(self, data):
        boolean_fields = [
            'has_previous_professor_position',
            'has_reviewed_teaching_material',
            'participated_in_international_mobility',
            'led_international_project',
            'received_award',
        ]

        for field in boolean_fields:
            if field not in data or data[field] is None:
                data[field] = False
            elif data[field] == 'true' or data[field] is True:
                data[field] = True
            else:
                data[field] = False

        return data