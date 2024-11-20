from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import (
    RegisterSerializer, CMSRegistrationSerializer,
    PredavacIzborSerializer,PredavacReizborSerializer, 
    VisiPredavacIzborSerializer, VisiPredavacReizborSerializer, 
    ProfesorStrucnogStudijaIzborSerializer, ProfesorStrucnogStudijaReizborSerializer, 
    ProfesorStrucnogStudijaTrajniSerializer,
    )

from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from rest_framework_simplejwt.authentication import JWTAuthentication   
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from .models import (
    PredavacIzborModel,PredavacReizborModel, 
    VisiPredavacIzborModel, VisiPredavacReizborModel, 
    ProfesorStrucnogStudijaIzborModel, ProfesorStrucnogStudijaReizborModel, ProfesorStrucnogStudijaTrajniModel, Prijava
    )
from django.contrib.auth import authenticate
from django.views import View
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q

class HomeView(TemplateView):
    template_name = 'home_page.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['positions'] = [
            {'id': 1, 'name': 'Predavač (izbor)'},
            {'id': 2, 'name': 'Predavač (reizbor)'},
            {'id': 3, 'name': 'Viši predavač (izbor)'},
            {'id': 4, 'name': 'Viši predavač (reizbor)'},
            {'id': 5, 'name': 'Profesor stručnog studija (izbor)'},
            {'id': 6, 'name': 'Profesor stručnog studija (reizbor)'},
            {'id': 7, 'name': 'Profesor stručnog studija u trajnom izboru'},
        ]
        return context

class CMSDashboardView(LoginRequiredMixin, View):
    login_url = '/admin-login/'

    def get(self, request):
        filter_position = request.GET.get('filter_position', '')
        order_by = request.GET.get('order_by', 'asc') 
        search_query = request.GET.get('search', '').strip() 


        sve_prijave = Prijava.objects.all()

 
        if filter_position:
            sve_prijave = sve_prijave.filter(prijava_tip=filter_position)


        if search_query:
            sve_prijave = sve_prijave.filter(
                Q(user__first_name__icontains=search_query) | 
                Q(user__last_name__icontains=search_query)
            )


        if order_by == 'asc':
            sve_prijave = sve_prijave.order_by('created_at')
        else:
            sve_prijave = sve_prijave.order_by('-created_at')


        prijave_podaci = []

        for prijava in sve_prijave:
            try:
                content_type = prijava.content_type
                model_klass = content_type.model_class()
                specific_prijava = model_klass.objects.get(id=prijava.object_id)

                prijave_podaci.append({
                    'id': prijava.id,
                    'ime': specific_prijava.user.first_name,
                    'prezime': specific_prijava.user.last_name,
                    'pozicija': prijava.prijava_tip,
                    'vrijeme_kreiranja': prijava.created_at,
                })
            except model_klass.DoesNotExist:
                continue

        context = {
            'sve_prijave': prijave_podaci,
            'filter_position': filter_position,
            'order_by': order_by,
            'search': search_query,
        }
        return render(request, 'CMS_Dashboard.html', context)

    
@method_decorator(login_required, name='dispatch')
class ApplicationDetailView(View):
    login_url = '/admin-login/'

    def get(self, request, id):

        try:
            prijava = Prijava.objects.get(id=id)
        except Prijava.DoesNotExist:
            return render(request, '404.html', status=404)

        model_class = prijava.content_type.model_class()
        try:
            spec_prijava = model_class.objects.get(id=prijava.object_id)
        except model_class.DoesNotExist:
            return render(request, '404.html', status=404)

        context = {
            'prijava': spec_prijava,
            'pozicija': prijava.prijava_tip,
            'prijava_id': prijava.id 
        }

        template_mapping = {
            "Predavač - Izbor": "application_detail_predavac_izbor.html",
            "Predavač - Reizbor": "application_detail_predavac_reizbor.html",
            "Viši predavač - Izbor": "application_detail_visi_predavac_izbor.html",
            "Viši predavač - Reizbor": "application_detail_visi_predavac_reizbor.html",
            "Profesor stručnog studija - Izbor": "application_detail_profesor_strucnog_studija_izbor.html",
            "Profesor stručnog studija - Reizbor": "application_detail_profesor_strucnog_studija_reizbor.html",
            "Profesor stručnog studija - Trajni": "application_detail_profesor_strucnog_studija_trajni.html",
        }

        template_name = template_mapping.get(prijava.prijava_tip)
        if not template_name:
            return render(request, '404.html', status=404)

        return render(request, template_name, context)

    def post(self, request, id):
        if 'delete' in request.POST:
            try:
                prijava = Prijava.objects.get(id=id)

                model_class = prijava.content_type.model_class()
                try:
                    specific_instance = model_class.objects.get(id=prijava.object_id)
                    specific_instance.delete() 
                except model_class.DoesNotExist:
                    messages.error(request, "Specifična prijava nije pronađena.")


                prijava.delete()
                messages.success(request, "Prijava i povezani podaci su uspješno izbrisani.")
                return redirect('admin_dashboard')

            except Prijava.DoesNotExist:
                messages.error(request, "Prijava nije pronađena.")
                return redirect('admin_dashboard')


    
class QuestionnaireRedirectView(APIView):

    def get(self, request, position_id):
        if position_id == 1:
            return redirect('predavac_izbor')
        elif position_id == 2:
            return redirect('predavac_reizbor')
        elif position_id == 3:
            return redirect('visi_predavac_izbor')
        elif position_id == 4:
            return redirect('visi_predavac_reizbor')
        elif position_id == 5:
            return redirect('profesor_strucnog_studija_izbor')
        elif position_id == 6:
            return redirect('profesor_strucnog_studija_reizbor')
        elif position_id == 7:
            return redirect('profesor_strucnog_studija_trajni')
        else:
            return Response({'error': 'Nepoznata pozicija.'}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'register.html', {})

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'register.html', {'success': True})
        else:
            return render(request, 'register.html', {'errors': serializer.errors, 'data': request.data})

class CMSRegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'CMS_Register.html', {})

    def post(self, request):
        serializer = CMSRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'CMS_Register.html', {'success': True})
        else:
            return render(request, 'CMS_Register.html', {'errors': serializer.errors, 'data': request.data})
    
        
@method_decorator(login_required, name='dispatch')
class PredavacIzborView(APIView):
    def get(self, request):
        return render(request, 'predavac_izbor.html')

    def post(self, request):
        data = request.data.copy()
        files = request.FILES

        data.update(files)

        serializer = PredavacIzborSerializer(data=data)

        if serializer.is_valid():
            nova_prijava = serializer.save(user=request.user)

            Prijava.objects.create(
                user=request.user,
                created_at=nova_prijava.created_at,
                content_type=ContentType.objects.get_for_model(PredavacIzborModel),
                object_id=nova_prijava.id,
                prijava_tip='Predavač - Izbor',
            )
            return render(request, 'success.html', {'message': 'Vaša prijava je uspješno zaprimljena.'})

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(login_required, name='dispatch')
class PredavacReizborView(APIView):
    def get(self, request):

        return render(request, 'predavac_reizbor.html')
    def post(self, request):
        data = request.data.copy()
        files = request.FILES


        data.update(files)


        checkbox_fields = ['is_elected_lecturer', 'project_leadership_experience']
        for field in checkbox_fields:
            data[field] = data.get(field, '') != ''


        serializer = PredavacReizborSerializer(data=data)

        if serializer.is_valid():

            nova_prijava = serializer.save(user=request.user)

            Prijava.objects.create(
                user=request.user,
                created_at=nova_prijava.created_at,
                content_type=ContentType.objects.get_for_model(PredavacReizborModel),
                object_id=nova_prijava.id,
                prijava_tip='Predavač - Reizbor',
            )
            return render(request, 'success.html', {'message': 'Vaša prijava je uspješno zaprimljena.'})

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class VisiPredavacIzborView(APIView):
    def get(self, request):

        return render(request, 'visi_predavac_izbor.html')
    def post(self, request):
        data = request.data.copy()
        files = request.FILES


        data.update(files)

        checkbox_fields = ['gatherings']
        for field in checkbox_fields:
            if field not in data or data[field] == '':
                data[field] = False
            else:
                data[field] = True

        serializer = VisiPredavacIzborSerializer(data=data)

        if serializer.is_valid():
            nova_prijava = serializer.save(user=request.user)

            Prijava.objects.create(
                user=request.user,
                created_at=nova_prijava.created_at,
                content_type=ContentType.objects.get_for_model(VisiPredavacIzborModel),
                object_id=nova_prijava.id,
                prijava_tip='Viši predavač - Izbor',
            )

            return render(request, 'success.html', {'message': 'Vaša prijava je uspješno zaprimljena.'})
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(login_required, name='dispatch')
class VisiPredavacReizborView(APIView):
    def get(self, request):

        return render(request, 'visi_predavac_reizbor.html')
    def post(self, request):
        data = request.data.copy()
        files = request.FILES


        data.update(files)


        serializer = VisiPredavacReizborSerializer(data=data)

        if serializer.is_valid():

            nova_prijava = serializer.save(user=request.user)


            Prijava.objects.create(
                user=request.user,
                created_at=nova_prijava.created_at,
                content_type=ContentType.objects.get_for_model(VisiPredavacReizborModel),
                object_id=nova_prijava.id,
                prijava_tip='Viši predavač - Reizbor',
            )
            return render(request, 'success.html', {'message': 'Vaša prijava je uspješno zaprimljena.'})

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class ProfesorStrucnogStudijaIzborView(APIView):
    def get(self, request):

        return render(request, 'profesor_strucnog_studija_izbor.html')
    def post(self, request):
        data = request.data.copy()
        files = request.FILES

        data.update(files)

        checkbox_fields = ['reviewed_teaching_material', 'participated_in_international_mobility', 
                           'led_international_project', 'received_international_award']
        for field in checkbox_fields:
            data[field] = data.get(field, '') != ''

        serializer = ProfesorStrucnogStudijaIzborSerializer(data=data)

        if serializer.is_valid():

            nova_prijava = serializer.save(user=request.user)


            Prijava.objects.create(
                user=request.user,
                created_at=nova_prijava.created_at,
                content_type=ContentType.objects.get_for_model(ProfesorStrucnogStudijaIzborModel),
                object_id=nova_prijava.id,
                prijava_tip='Profesor stručnog studija - Izbor',
            )
            return render(request, 'success.html', {'message': 'Vaša prijava je uspješno zaprimljena.'})

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class ProfesorStrucnogStudijaReizborView(APIView):
    def get(self, request):

        return render(request, 'profesor_strucnog_studija_reizbor.html')
    def post(self, request):
        data = request.data.copy()
        files = request.FILES

        data.update(files)


        checkbox_fields = ['has_reviewed_teaching_material', 'participated_in_international_mobility', 
                           'led_international_project', 'received_award']
        for field in checkbox_fields:
            data[field] = data.get(field, '') != ''

        serializer = ProfesorStrucnogStudijaReizborSerializer(data=data)

        if serializer.is_valid():

            nova_prijava = serializer.save(user=request.user)


            Prijava.objects.create(
                user=request.user,
                created_at=nova_prijava.created_at,
                content_type=ContentType.objects.get_for_model(ProfesorStrucnogStudijaReizborModel),
                object_id=nova_prijava.id,
                prijava_tip='Profesor stručnog studija - Reizbor',
            )
            return render(request, 'success.html', {'message': 'Vaša prijava je uspješno zaprimljena.'})

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(login_required, name='dispatch')
class ProfesorStrucnogStudijaTrajniView(APIView):
    
    def get(self, request):
        return render(request, 'profesor_strucnog_studija_trajni.html')

    def post(self, request):
        data = request.data.copy()
        files = request.FILES

        data.update(files)

        checkbox_fields = ['has_previous_professor_position', 'has_reviewed_teaching_material', 
                           'participated_in_international_mobility', 'led_international_project', 
                           'received_award']
        for field in checkbox_fields:
            data[field] = data.get(field, '') != ''

        serializer = ProfesorStrucnogStudijaTrajniSerializer(data=data)

        if serializer.is_valid():

            nova_prijava = serializer.save(user=request.user)


            Prijava.objects.create(
                user=request.user,
                created_at=nova_prijava.created_at,
                content_type=ContentType.objects.get_for_model(ProfesorStrucnogStudijaTrajniModel),
                object_id=nova_prijava.id,
                prijava_tip='Profesor stručnog studija - Trajni',
            )
            return render(request, 'success.html', {'message': 'Vaša prijava je uspješno zaprimljena.'})

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    