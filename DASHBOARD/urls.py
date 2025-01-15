from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard' ),
    path('search',views.search,name='search' ),
    path('export_folder_data/<int:folder_id>',views.export_folder_data,name='export_folder_data' ),
    path('add_company',views.AddCompany.as_view(),name='add_company' ),
    path('add_employee',views.AddEmployee.as_view(),name='add_employee' ),
    path('add_convention',views.AddConvention.as_view(),name='add_convention' ),
    path('add_setting',views.AddSetting.as_view(),name='add_setting' ),
    path('add_folder',views.AddFolder.as_view(),name='add_folder' ),
    path('update_company/<int:pk>',views.UpdateCompany.as_view(),name='update_company' ),
    path('update_employee/<int:pk>',views.UpdateEmployee.as_view(),name='update_employee' ),
    path('update_convention/<int:pk>',views.UpdateConvention.as_view(),name='update_convention' ),
    path('update_setting/<int:pk>',views.UpdateSetting.as_view(),name='update_setting' ),
    path('update_folder/<int:pk>',views.UpdateFolder.as_view(),name='update_folder' ),
    path('delete_company/<int:pk>',views.DeleteCompany.as_view(),name='delete_company' ),
    path('delete_employee/<int:pk>',views.DeleteEmployee.as_view(),name='delete_employee' ),
    path('delete_convention/<int:pk>',views.DeleteConvention.as_view(),name='delete_convention' ),
    path('delete_setting/<int:pk>',views.DeleteSetting.as_view(),name='delete_setting' ),
    path('delete_folder/<int:pk>',views.DeleteFolder.as_view(),name='delete_folder' ),
]