"""
Views adaptadas para usar Supabase REST API
Substitui as views originais que usavam PostgreSQL direto
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Importar o cliente Supabase
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from supabase_client import supabase_client

@login_required
def painel_usuario(request):
    """Painel principal do usuário usando Supabase API"""
    try:
        # Buscar dados do usuário no Supabase
        usuarios = supabase_client.select('usuarios')
        pallets = supabase_client.select('pallets')
        vales = supabase_client.select('vales')
        
        # Estatísticas
        total_usuarios = len(usuarios)
        total_pallets = len(pallets)
        total_vales = len(vales)
        
        context = {
            'usuarios': usuarios,
            'pallets': pallets,
            'vales': vales,
            'total_usuarios': total_usuarios,
            'total_pallets': total_pallets,
            'total_vales': total_vales,
        }
        
        return render(request, 'painel_usuario.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao carregar dados: {str(e)}')
        return render(request, 'painel_usuario.html', {'error': True})

@login_required
def criar_usuario(request):
    """Criar novo usuário no Supabase"""
    if request.method == 'POST':
        try:
            data = {
                'nome': request.POST.get('nome'),
                'email': request.POST.get('email'),
                'telefone': request.POST.get('telefone', ''),
                'ativo': True,
                'created_at': 'now()'
            }
            
            # Inserir no Supabase
            resultado = supabase_client.insert('usuarios', data)
            
            if resultado:
                messages.success(request, 'Usuário criado com sucesso!')
                return redirect('painel_usuario')
            else:
                messages.error(request, 'Erro ao criar usuário')
                
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
    
    return render(request, 'criar_usuario.html')

@login_required
def listar_pallets(request):
    """Listar pallets do Supabase"""
    try:
        # Buscar pallets com filtros se necessário
        filtros = {}
        if request.GET.get('status'):
            filtros['status'] = request.GET.get('status')
        
        pallets = supabase_client.select('pallets', filters=filtros)
        
        context = {
            'pallets': pallets,
            'status_filter': request.GET.get('status', '')
        }
        
        return render(request, 'listar_pallets.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao carregar pallets: {str(e)}')
        return render(request, 'listar_pallets.html', {'error': True})

@login_required
def criar_pallet(request):
    """Criar novo pallet no Supabase"""
    if request.method == 'POST':
        try:
            data = {
                'codigo': request.POST.get('codigo'),
                'descricao': request.POST.get('descricao'),
                'status': request.POST.get('status', 'ativo'),
                'usuario_id': request.user.id,
                'created_at': 'now()'
            }
            
            resultado = supabase_client.insert('pallets', data)
            
            if resultado:
                messages.success(request, 'Pallet criado com sucesso!')
                return redirect('listar_pallets')
            else:
                messages.error(request, 'Erro ao criar pallet')
                
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
    
    return render(request, 'criar_pallet.html')

@login_required
def gerar_vale(request):
    """Gerar vale no Supabase"""
    if request.method == 'POST':
        try:
            data = {
                'codigo': request.POST.get('codigo'),
                'valor': float(request.POST.get('valor', 0)),
                'descricao': request.POST.get('descricao'),
                'status': 'ativo',
                'usuario_id': request.user.id,
                'created_at': 'now()'
            }
            
            resultado = supabase_client.insert('vales', data)
            
            if resultado:
                messages.success(request, 'Vale gerado com sucesso!')
                return redirect('listar_vales')
            else:
                messages.error(request, 'Erro ao gerar vale')
                
        except Exception as e:
            messages.error(request, f'Erro: {str(e)}')
    
    return render(request, 'gerar_vale.html')

@login_required
def listar_vales(request):
    """Listar vales do Supabase"""
    try:
        # Buscar vales do usuário
        filtros = {'usuario_id': request.user.id}
        if request.GET.get('status'):
            filtros['status'] = request.GET.get('status')
        
        vales = supabase_client.select('vales', filters=filtros)
        
        context = {
            'vales': vales,
            'status_filter': request.GET.get('status', '')
        }
        
        return render(request, 'listar_vales.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao carregar vales: {str(e)}')
        return render(request, 'listar_vales.html', {'error': True})

@csrf_exempt
def api_status(request):
    """API para verificar status da conexão Supabase"""
    try:
        # Teste simples de conectividade
        test_data = supabase_client.select('usuarios', columns='id', filters={'id': 1})
        
        return JsonResponse({
            'status': 'ok',
            'supabase_connected': True,
            'message': 'Conexão com Supabase funcionando'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'supabase_connected': False,
            'message': f'Erro na conexão: {str(e)}'
        }, status=500)

@login_required
def dashboard_stats(request):
    """Dashboard com estatísticas do Supabase"""
    try:
        # Contar registros
        total_usuarios = supabase_client.count('usuarios')
        total_pallets = supabase_client.count('pallets')
        total_vales = supabase_client.count('vales')
        
        # Vales por status
        vales_ativos = supabase_client.count('vales', {'status': 'ativo'})
        vales_usados = supabase_client.count('vales', {'status': 'usado'})
        
        context = {
            'stats': {
                'total_usuarios': total_usuarios,
                'total_pallets': total_pallets,
                'total_vales': total_vales,
                'vales_ativos': vales_ativos,
                'vales_usados': vales_usados,
            }
        }
        
        return render(request, 'dashboard_stats.html', context)
        
    except Exception as e:
        messages.error(request, f'Erro ao carregar estatísticas: {str(e)}')
        return render(request, 'dashboard_stats.html', {'error': True})

