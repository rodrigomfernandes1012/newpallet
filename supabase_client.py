import os
import requests
from typing import Dict, List, Any, Optional

class SupabaseClient:
    """Cliente Supabase usando REST API para bypass do problema IPv6"""
    
    def __init__(self):
        self.url = os.environ.get('SUPABASE_URL', 'https://zyeaqpsltgavouygatxs.supabase.co')
        self.key = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5ZWFxcHNsdGdhdm91eWdhdHhzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc4MjQ4NDMsImV4cCI6MjA2MzQwMDg0M30.L9SVkjKQk2cVygHIIcjC0T9YQ_SEZXRUvSSMOYhDWvE')
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def select(self, table: str, columns: str = '*', filters: Optional[Dict] = None) -> List[Dict]:
        """Buscar dados de uma tabela"""
        url = f"{self.url}/rest/v1/{table}"
        params = {'select': columns}
        
        if filters:
            for key, value in filters.items():
                params[f"{key}"] = f"eq.{value}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados: {e}")
            return []
    
    def insert(self, table: str, data: Dict) -> Optional[Dict]:
        """Inserir dados em uma tabela"""
        url = f"{self.url}/rest/v1/{table}"
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result[0] if result else None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao inserir dados: {e}")
            return None
    
    def update(self, table: str, filters: Dict, data: Dict) -> Optional[List[Dict]]:
        """Atualizar dados em uma tabela"""
        url = f"{self.url}/rest/v1/{table}"
        params = {}
        
        for key, value in filters.items():
            params[f"{key}"] = f"eq.{value}"
        
        try:
            response = requests.patch(url, headers=self.headers, params=params, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar dados: {e}")
            return None
    
    def delete(self, table: str, filters: Dict) -> bool:
        """Deletar dados de uma tabela"""
        url = f"{self.url}/rest/v1/{table}"
        params = {}
        
        for key, value in filters.items():
            params[f"{key}"] = f"eq.{value}"
        
        try:
            response = requests.delete(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao deletar dados: {e}")
            return False
    
    def count(self, table: str, filters: Optional[Dict] = None) -> int:
        """Contar registros em uma tabela"""
        url = f"{self.url}/rest/v1/{table}"
        headers = {**self.headers, 'Prefer': 'count=exact'}
        params = {'select': 'id'}
        
        if filters:
            for key, value in filters.items():
                params[f"{key}"] = f"eq.{value}"
        
        try:
            response = requests.head(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return int(response.headers.get('Content-Range', '0').split('/')[-1])
        except (requests.exceptions.RequestException, ValueError):
            return 0

# Instância global
supabase_client = SupabaseClient()

