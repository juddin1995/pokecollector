from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemon/', views.index, name='pokemon-index'),
    path('pokemon/<int:poke_id>/', views.poke_detail, name='poke-detail'),
    path('pokemon/<int:poke_id>/catch', views.catch_pokemon, name='catch-pokemon'),
    path('pokemon/show', views.show_pokemon, name='show-pokemon'),
    path('pokemon/<int:pk>/delete/', views.PokemonDeleteView.as_view(), name='pokemon-delete'),
    path('pokemon/<int:poke_id>/update-nickname/', views.update_nickname, name='update-nickname'),
    path('pokemon/<int:poke_id>/add-feeding/', views.add_feeding, name='add-feeding'),
    path('items/create/', views.ItemCreate.as_view(), name='item-create'),
    path('items/<int:pk>/', views.ItemDetail.as_view(), name='item-detail'),
    path('items/', views.ItemList.as_view(), name='item-index'),
    path('items/<int:pk>/update/', views.ItemUpdate.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', views.ItemDelete.as_view(), name='item-delete'),
    path('items/<int:poke_id>/assoc-item/<int:item_id>/', views.assoc_item, name='assoc-item'),
    path('pokemon/<int:poke_id>/remove-item/<int:item_id>', views.remove_item, name='remove-item'),
]