#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conexión con la API de ModelScope
https://modelscope.cn/openapi/v1

Este script demuestra cómo conectarse y hacer solicitudes a la API de ModelScope.
"""

import requests
import json
import os
from typing import Optional, Dict, Any


class ModelScopeClient:
    """Cliente para interactuar con la API de ModelScope."""
    
    BASE_URL = "https://modelscope.cn/openapi/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de ModelScope.
        
        Args:
            api_key: Tu clave de API de ModelScope. 
                    También puede establecerse mediante la variable de entorno MODELSCOPE_API_KEY.
        """
        self.api_key = api_key or os.getenv("MODELSCOPE_API_KEY")
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Realiza una solicitud HTTP a la API.
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            endpoint: Endpoint de la API (ej: "/models")
            params: Parámetros de consulta
            data: Datos del cuerpo de la solicitud
            
        Returns:
            Respuesta de la API como diccionario
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Estado: {e.response.status_code}")
                print(f"Respuesta: {e.response.text}")
            raise
    
    def get_models(self, limit: int = 10) -> Dict[str, Any]:
        """
        Obtiene una lista de modelos disponibles.
        
        Args:
            limit: Número máximo de modelos a retornar
            
        Returns:
            Lista de modelos
        """
        params = {"limit": limit}
        return self._make_request("GET", "/models", params=params)
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un modelo específico.
        
        Args:
            model_id: ID del modelo
            
        Returns:
            Información del modelo
        """
        return self._make_request("GET", f"/models/{model_id}")
    
    def test_connection(self) -> bool:
        """
        Prueba la conexión con la API.
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            # Intentar hacer una solicitud simple
            response = self._make_request("GET", "/")
            print("✓ Conexión exitosa con ModelScope API")
            print(f"Respuesta: {json.dumps(response, indent=2, ensure_ascii=False)}")
            return True
        except Exception as e:
            print(f"✗ Error al conectar: {e}")
            return False


def main():
    """Función principal para demostrar el uso del cliente."""
    
    print("=" * 60)
    print("Conexión con ModelScope API")
    print("URL Base: https://modelscope.cn/openapi/v1")
    print("=" * 60)
    
    # Crear instancia del cliente
    # Nota: Para funcionalidades completas, necesitarás una API key válida
    # Puedes obtenerla en: https://modelscope.cn/my/myaccesstoken
    client = ModelScopeClient()
    
    # Probar conexión
    print("\n1. Probando conexión...")
    client.test_connection()
    
    # Ejemplo: Buscar modelos (puede requerir autenticación)
    print("\n2. Buscando modelos disponibles...")
    try:
        models = client.get_models(limit=5)
        print(f"Modelos encontrados: {json.dumps(models, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"Nota: Esta operación puede requerir autenticación. Error: {e}")
    
    print("\n" + "=" * 60)
    print("Instrucciones:")
    print("1. Obtén tu API Key en: https://modelscope.cn/my/myaccesstoken")
    print("2. Establece la variable de entorno: export MODELSCOPE_API_KEY='tu_key'")
    print("3. O pasa la key directamente: ModelScopeClient(api_key='tu_key')")
    print("=" * 60)


if __name__ == "__main__":
    main()
