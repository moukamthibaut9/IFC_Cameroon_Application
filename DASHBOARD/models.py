from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator
from decimal import Decimal
import math


juridical_statuses = [('SARL','SARL'),('SA','SA'),('SCS/SCA','SCS/SCA'),('SNC','SNC'),('SAS','SAS'),('Autres','Autres')]
activities_soctors =[
    ('IND-FAB','Industrie et Fabrication'), ('TECH-INNOV','Technologies et Innovation'),
    ('SANTE-BE','Santé et Bien-être'), ('CREA-CUL','Creation et Culture'), ('FIN','Finance'),
    ('ENV-AGR','Environnement et Agriculture'), ('COM-DIST','Commerce et Distribution'),
    ('TOUR-HOT','Tourisme et Hôtellerie'), ('EDUC-FORM','Education et Formation'), ('AUT','Autre')
]
socio_professional_categories=[
    ('SG','Stagiaire'),('ASC','Assistant/Collaborateur'),('OV','Ouvrier'),('TEC','Technicien'),
    ('CI','Cadre Intermediaire'),('CS','Cadre Superieur'),('DIR','Dirrigeant'),('FR','Freelance'),
    ('FP','Fonctionnaire(secteur publique uniquement)'),('AT','Autres')
]
convention_types =[
    ('C-SEC_COM','Convention du secteur commercial'), ('C-SEC_MIN','Convention du secteur minier'),
    ('C-SEC_PET','Convention du secteur pretrolier'), ('C-SEC_SAN','Convention du secteur sanitaire'),
    ('C-SEC_AGR','Convention du secteur agricole'),('C-SEC_EDU','Convention du secteur éducatif'),
    ('C-SEC_TEC','Convention du secteur technologique'),('C-SEC_TOU','Convention du secteur touristique'),
    ('C-SEC_CUL','Convention du secteur culturel'),('C-SEC_AUT','Convention d\'un autre secteur d\'activité'),
    ('C-IAS19','Convention selon la norme IAS 19'),('C-AUT','Convention selon une autre norme')
]
folders_statuses = [('CRE', 'Créé'),('VAL', 'Validé'),('SIM', 'Simulé'),('ABN', 'Abandonné'),('SUP', 'Supprimé')]


class Company(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    company_name = models.CharField(max_length=150,blank=False)
    director_name = models.CharField(max_length=150,blank=True)
    status = models.CharField(max_length=10,choices=juridical_statuses,default='SARL',blank=False)
    activity_sector = models.CharField(max_length=15,choices=activities_soctors,blank=False)
    localisation = models.CharField(
        max_length=200,
        validators=[RegexValidator(r'^([A-Za-zÀ-ÿ\s-]{2,40})/([A-Za-zÀ-ÿ\s-]{2,40})/([A-Za-zÀ-ÿ0-9\s-]{2,40})/([A-Za-zÀ-ÿ0-9\s-]{2,80})$')],
        help_text="(Au format : Pays/Ville/Quartier/Rue)",
    )
    nbr_employees=models.PositiveBigIntegerField(blank=False)
    tel_contact = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?[1-9]\d{1,14}$', 'Numéro de téléphone invalide')],
        blank=True
    )
    email_contact = models.EmailField(max_length=150,blank=False)
    birth_date = models.DateField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class Convention(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=150,choices=convention_types,blank=False,unique=True)
    compute_parameters_detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_name_display()}"


class Setting(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    # Choix d'une convention
    convention = models.OneToOneField(Convention,on_delete=models.CASCADE)
    # Nombre d'annees d'anciennete minimal avant que l'employe puisse beneficier d'une IFC
    base_seniority = models.PositiveSmallIntegerField(validators=[MaxValueValidator(12)],default=5)
        #*****Parametres relatifs au calcul de l'IFC selon la convention du secteur d'activite*****
    # Taux d'indemnité de base
    base_compensation_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.2
    )
    # Nombre d'annees d'attente avant augmentation du taux d'indemnité
    years_gap = models.PositiveSmallIntegerField(validators=[MaxValueValidator(8)],default=5)
    # valeur de l'augmentation du taux d'indemnité a chaque fois
    add_compensation_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.05
    )
        #*****Parametres relatifs au calcul de l'IFC selon la convention de la norme IAS19*****
    # Taux utilisé pour actualiser les paiements futurs d'un employe
    discount_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.03
    )
    # Taux d'augmentation annuelle du salaire de l'employé (inflation salariale)
    wage_inflation_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        default=0.05
    )
    # Age auquel l'employe doit normalement prendre sa retraite
    employee_retirement_age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(65)],default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parametrage pour la {self.convention.get_name_display().lower()}"


class Employee(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=150,blank=False)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200)])
    identifier = models.CharField(
        max_length=10,
        help_text="(Une chaine de 10 caracteres pouvant etre uniquement des lettres ou des chiffres)",
        validators=[RegexValidator(r'^[A-Za-z0-9]{10}$')],
        unique=True)
    seniority = models.PositiveSmallIntegerField()
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    socio_professional_category = models.CharField(max_length=5,choices=socio_professional_categories,blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Folder(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=folders_statuses)
    ifc_result = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def employee_ifc_compute(self):
        """
        Cette méthode calcule l'IFC de l'employé en fonction de la convention et du statut.
        Le résultat est ensuite stocké dans le champ `ifc_result`.
        """
        if self.setting.convention.name[:5] == 'C-SEC':
            # Aciennete(seniority) a considerer pour le calcul de l'IFC selon le statut du dossier de l'employe
            if self.status == 'SIM':
                # Ici, on considere l'anciennete qu'aura l'employe s'il atteint l'age de la retraite au sein de la societe
                seniority = self.employee.seniority + (self.setting.employee_retirement_age - self.employee.age)
            else:
                # Dans les autres cas, on considere l'anciennete reelle de l'employe
                seniority = self.employee.seniority 
            if self.status in ['VAL','SIM']:
                if self.status == 'VAL' and self.employee.seniority < self.setting.base_seniority:
                    self.ifc_result = 0
                else:
                    # Evaluation de son IFC (  Formule: IFC = taux_indemnite * anciennete * salaire  )
                    self.ifc_result = (self.setting.base_compensation_rate + \
                            ((seniority - self.setting.base_seniority)//self.setting.years_gap)* \
                            self.setting.add_compensation_rate)*seniority*self.employee.base_salary
            else:
                # Si le dossier est juste créé, abandonné ou supprimé, on ne calcule rien
                self.ifc_result = 0
        else:
            # Nombre d'annees restants a l'employe pour la prise de retraite
            n = self.setting.employee_retirement_age - self.employee.age
            # Salaire annuel estimé de l'employe a partir de son salaire de base actuel
            annual_salary = 12*self.employee.base_salary
            # Evaluation de son IFC a la retraite (  Formule: IFC = S0*(1+g)^n  )
            retirement_ifc_amount = annual_salary*Decimal(math.pow(1+self.setting.wage_inflation_rate,n))
            # Evaluation de son IFC actuel (  Formule: IFC = retirement_ifc_amount/(1+r)^n  )
            actual_ifc_amount = retirement_ifc_amount/Decimal(math.pow(1+self.setting.discount_rate,n))
            if self.status == 'VAL':
                # Calcul de la valeur réelle de l'IFC
                if self.employee.seniority >= self.setting.base_seniority:
                    self.ifc_result = actual_ifc_amount
                else:
                    self.ifc_result = 0
            elif self.status == 'SIM':
                # Valeur simulée de l'IFC (Hyphothese de l'age de la retraite atteinte)
                self.ifc_result = retirement_ifc_amount
            else:
                # Si le dossier est juste créé, abandonné ou supprimé, on ne calcule rien
                self.ifc_result = 0
        # Sauvegarde du résultat dans la base de données
        self.save()

    def __str__(self):
        return f"Dossier N°:{self.employee.identifier} de l'employe: {self.employee.name}"
