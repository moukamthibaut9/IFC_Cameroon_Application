from django import forms
from .models import Company,Convention,Setting,Employee,Folder

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'company_name','director_name','status','activity_sector','localisation',
            'nbr_employees','tel_contact','email_contact','birth_date'
        ]
        labels = {
            'company_name':'Nom de la société',
            'director_name':'Nom du PDG de la société',
            'status':'Statut juridique',
            'activity_sector':'Secteur d\'activité',
            'localisation':'Où se trouve le siège de la sosiété?',
            'nbr_employees':'Combien d\'employés dans cette société?',
            'tel_contact':'Numéro de téléphone de service de la société',
            'email_contact':'Adresse e-mail de la société',
            'birth_date':'Date de création de la société'
        }
        widgets = {
            'company_name':forms.TextInput(attrs={'class':'form-control'}),
            'director_name':forms.TextInput(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'activity_sector':forms.Select(attrs={'class':'form-control'}),
            'localisation':forms.TextInput(attrs={'placeholder':'Ex: Cameroun/Maroua/Frolina/Elevage','class':'form-control'}),
            'nbr_employees':forms.NumberInput(attrs={'class':'form-control'}),
            'tel_contact':forms.TextInput(attrs={'type':'tel','class':'form-control'}),
            'email_contact':forms.EmailInput(attrs={'class':'form-control'}),
            'birth_date':forms.DateInput(attrs={'type':'date','class':'form-control'})
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name','age','identifier','seniority','base_salary',
            'socio_professional_category','company',
        ]
        labels = {
            'name':'Nom de l\'employé',
            'age':'Age de l\'employé',
            'identifier':'Identifiant de l\'employé',
            'seniority':'Ancienneté',
            'base_salary':'Salaire de base',
            'socio_professional_category':'Catégorie socio-professionnel',
            'company':'Société d\'appartenance de l\'employé',
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'age':forms.NumberInput(attrs={'class':'form-control'}),
            'identifier':forms.TextInput(attrs={'placeholder':'Ex: E0200sdp12','class':'form-control'}),
            'seniority':forms.NumberInput(attrs={'class':'form-control'}),
            'base_salary':forms.NumberInput(attrs={'min':'0','class':'form-control'}),
            'socio_professional_category':forms.Select(attrs={'class':'form-control'}),
            'company':forms.Select(attrs={'class':'form-control'}),
        }


class ConventionForm(forms.ModelForm):
    class Meta:
        model = Convention
        fields = ['name','compute_parameters_detail']
        labels = {
            'name':'Selectionnez une convention',
            'compute_parameters_detail':'Détails sur les paramètres associés pour le calcul de l\'IFC'
        }
        widgets = {
            'name':forms.Select(attrs={'class':'form-control'}),
            'compute_parameters_detail':forms.Textarea(attrs={'class':'form-control'})
        }


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields =[
            'convention','base_seniority','base_compensation_rate','years_gap',
            'add_compensation_rate','discount_rate','wage_inflation_rate','employee_retirement_age',
        ]
        labels = {
            'convention':'A quelle convention sera associé ce parametrage?',
            'base_seniority':'Quelle ancienneté minimale doit avoir un employé pour bénéficier d\'une IFC?',
            'base_compensation_rate':'Définissez le taux d\'indemnité correspondant à l\'ancienneté minimale ci-dessus',
            'years_gap':'Nombre d\'années minimal qui doivent s\'écouler avant augmentation du taux d\'indemnité',
            'add_compensation_rate':'Valeur de l\'augmentation du taux d\'indemnité après chaque nombre d\'années précédement défini',
            'discount_rate':'Définissez une valeur pour le taux d\'actualisation des paiements futurs',
            'wage_inflation_rate':'Définissez une valeur pour le taux d\'inflation salariale',
            'employee_retirement_age':'Quel est l\'age de retraite prévu pour un employé?', 
            
        }
        widgets = {
            'convention':forms.Select(attrs={'class':'form-control'}),
            'base_seniority':forms.NumberInput(attrs={'class':'form-control'}),
            'base_compensation_rate':forms.NumberInput(attrs={'min':'0','max':'1','class':'form-control'}),
            'years_gap':forms.NumberInput(attrs={'class':'form-control'}),
            'add_compensation_rate':forms.NumberInput(attrs={'min':'0','max':'1','class':'form-control'}),
            'discount_rate':forms.NumberInput(attrs={'min':'0','max':'1','class':'form-control'}),
            'wage_inflation_rate':forms.NumberInput(attrs={'min':'0','max':'1','class':'form-control'}),
            'employee_retirement_age':forms.NumberInput(attrs={'class':'form-control'}), 
            
        }

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['employee','setting','status','ifc_result',]
        labels = {
            'employee':'Selectionnez l\'employé conserné par ce dossier',
            'setting':'Quel parametrage pour la convention de calcul de son IFC',
            'status':'Choisissez un statut pour ce dossier',
            'ifc_result':'Résultat du calcul de son IFC',
        }
        widgets = {
            'employee':forms.Select(attrs={'class':'form-control'}),
            'setting':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'ifc_result':forms.NumberInput(attrs={
                'placeholder':'Vous ne pouvez modifier ce champ',
                'class':'form-control',
                'disabled':'disabled'}),
        }
        
