class Compatibility:
    """Modelo para manejar compatibilidad entre juegos y hardware con sistema de puntuación"""

    # Tablas de rendimiento para comparación
    CPU_PERFORMANCE = {
        'intel': {
            'i9': 100, 'i7': 85, 'i5': 70, 'i3': 50, 'pentium': 30, 'celeron': 20
        },
        'amd': {
            'ryzen 9': 100, 'ryzen 7': 85, 'ryzen 5': 70, 'ryzen 3': 50, 'athlon': 30
        }
    }
    
    GPU_PERFORMANCE = {
        'nvidia': {
            'rtx 4090': 100, 'rtx 4080': 95, 'rtx 4070': 85, 'rtx 4060': 75,
            'rtx 3090': 90, 'rtx 3080': 85, 'rtx 3070': 75, 'rtx 3060': 65,
            'rtx 2080': 70, 'rtx 2070': 60, 'rtx 2060': 50,
            'gtx 1660': 45, 'gtx 1650': 40, 'gtx 1080': 55, 'gtx 1070': 50,
            'gtx 1060': 45, 'gtx 980': 40, 'gtx 970': 35, 'gtx 960': 30,
            'gtx 780': 25, 'gtx 770': 22, 'gtx 760': 20, 'gtx 660': 18,
            'gt 730': 10
        },
        'amd': {
            'rx 7900': 95, 'rx 7800': 85, 'rx 7700': 75, 'rx 7600': 65,
            'rx 6900': 85, 'rx 6800': 75, 'rx 6700': 65, 'rx 6600': 55,
            'rx 5700': 60, 'rx 5600': 50, 'rx 5500': 45,
            'rx 590': 40, 'rx 580': 38, 'rx 570': 35
        }
    }

    @classmethod
    def verificar_compatibility_completa(cls, juegos, componentes_seleccionados):
        """
        Verificar compatibilidad completa entre juegos seleccionados y componentes de hardware
        con sistema de puntuación mejorado

        Args:
            juegos: Lista de juegos seleccionados
            componentes_seleccionados: Lista de componentes de hardware seleccionados

        Returns:
            dict: Resultado de compatibilidad con detalles y puntuación
        """
        resultado = {
            "compatible": True,
            "detalles": [],
            "recomendaciones": [],
            "puntuacion_general": 0,
            "nivel_rendimiento": ""  # bajo, medio, alto, ultra
        }

        puntuaciones = []

        # Verificar cada juego contra cada componente
        for juego in juegos:
            for componente in componentes_seleccionados:
                compatibilidad = cls._verificar_juego_componente(juego, componente)
                resultado["detalles"].append({
                    "juego": juego.nombre,
                    "componente": f"{componente.marca} {componente.modelo}",
                    "tipo_componente": componente.tipo,
                    "compatible": compatibilidad["compatible"],
                    "razon": compatibilidad["razon"],
                    "puntuacion": compatibilidad.get("puntuacion", 0)
                })

                if not compatibilidad["compatible"]:
                    resultado["compatible"] = False
                
                if "puntuacion" in compatibilidad:
                    puntuaciones.append(compatibilidad["puntuacion"])
        
        # Calcular puntuación general
        if puntuaciones:
            resultado["puntuacion_general"] = sum(puntuaciones) / len(puntuaciones)
            
            # Determinar nivel de rendimiento
            if resultado["puntuacion_general"] >= 80:
                resultado["nivel_rendimiento"] = "ultra"
            elif resultado["puntuacion_general"] >= 60:
                resultado["nivel_rendimiento"] = "alto"
            elif resultado["puntuacion_general"] >= 40:
                resultado["nivel_rendimiento"] = "medio"
            else:
                resultado["nivel_rendimiento"] = "bajo"
        
        # Generar recomendaciones inteligentes
        resultado["recomendaciones"] = cls._generar_recomendaciones(
            componentes_seleccionados, 
            resultado["puntuacion_general"]
        )

        return resultado

    @classmethod
    def _verificar_juego_componente(cls, juego, componente):
        """Verificar compatibilidad entre un juego específico y un componente con puntuación"""
        resultado = {
            "compatible": True,
            "razon": "Compatible",
            "puntuacion": 0
        }

        # Verificar según el tipo de componente
        if componente.tipo == "CPU":
            resultado = cls._verificar_cpu_juego(juego, componente)
        elif componente.tipo == "GPU":
            resultado = cls._verificar_gpu_juego(juego, componente)
        elif componente.tipo == "RAM":
            resultado = cls._verificar_ram_juego(juego, componente)

        return resultado

    @classmethod
    def _verificar_cpu_juego(cls, juego, cpu):
        """Verificar compatibilidad entre CPU y juego con puntuación"""
        # Obtener requisitos
        if hasattr(juego, 'get_requisitos_minimos'):
            requisitos_cpu = juego.get_requisitos_minimos().get("CPU", "")
        else:
            requisitos_cpu = juego.requisitos_minimos.get("CPU", "")
        
        # Calcular puntuación del CPU del usuario
        cpu_score = cls._calcular_cpu_score(cpu.marca, cpu.modelo)
        
        # Calcular puntuación requerida
        required_score = cls._calcular_cpu_score_from_string(requisitos_cpu)
        
        if cpu_score >= required_score:
            # Calcular porcentaje de rendimiento
            if required_score > 0:
                performance_ratio = (cpu_score / required_score) * 100
                performance_ratio = min(performance_ratio, 100)
            else:
                performance_ratio = 100
            
            return {
                "compatible": True,
                "razon": f"CPU compatible - Rendimiento: {performance_ratio:.0f}%",
                "puntuacion": performance_ratio
            }
        else:
            return {
                "compatible": False,
                "razon": f"CPU insuficiente. Requiere: {requisitos_cpu}",
                "puntuacion": (cpu_score / required_score * 100) if required_score > 0 else 0
            }

    @classmethod
    def _verificar_gpu_juego(cls, juego, gpu):
        """Verificar compatibilidad entre GPU y juego con puntuación"""
        # Obtener requisitos
        if hasattr(juego, 'get_requisitos_minimos'):
            requisitos_gpu = juego.get_requisitos_minimos().get("GPU", "")
        else:
            requisitos_gpu = juego.requisitos_minimos.get("GPU", "")
        
        # Calcular puntuación de la GPU del usuario
        gpu_score = cls._calcular_gpu_score(gpu.marca, gpu.modelo)
        
        # Calcular puntuación requerida
        required_score = cls._calcular_gpu_score_from_string(requisitos_gpu)
        
        if gpu_score >= required_score:
            # Calcular porcentaje de rendimiento
            if required_score > 0:
                performance_ratio = (gpu_score / required_score) * 100
                performance_ratio = min(performance_ratio, 100)
            else:
                performance_ratio = 100
            
            return {
                "compatible": True,
                "razon": f"GPU compatible - Rendimiento: {performance_ratio:.0f}%",
                "puntuacion": performance_ratio
            }
        else:
            return {
                "compatible": False,
                "razon": f"GPU insuficiente. Requiere: {requisitos_gpu}",
                "puntuacion": (gpu_score / required_score * 100) if required_score > 0 else 0
            }

    @classmethod
    def _verificar_ram_juego(cls, juego, ram):
        """Verificar compatibilidad entre RAM y juego con puntuación"""
        # Extraer cantidad de RAM requerida y disponible
        if hasattr(juego, 'get_requisitos_minimos'):
            ram_requerida = cls._extraer_gb_ram(juego.get_requisitos_minimos().get("RAM", "0"))
        else:
            ram_requerida = cls._extraer_gb_ram(juego.requisitos_minimos.get("RAM", "0"))
        
        if hasattr(ram, 'get_especificaciones'):
            ram_disponible = cls._extraer_gb_ram(ram.get_especificaciones().get("capacidad", "0"))
        else:
            ram_disponible = cls._extraer_gb_ram(ram.especificaciones.get("capacidad", "0"))

        if ram_requerida > ram_disponible:
            puntuacion = (ram_disponible / ram_requerida) * 100 if ram_requerida > 0 else 0
            return {
                "compatible": False,
                "razon": f"RAM insuficiente. Requiere {ram_requerida}GB, tienes {ram_disponible}GB",
                "puntuacion": puntuacion
            }

        # Calcular puntuación basada en exceso de RAM
        if ram_requerida > 0:
            ratio = ram_disponible / ram_requerida
            if ratio >= 2:
                puntuacion = 100
            else:
                puntuacion = 50 + (ratio - 1) * 50
        else:
            puntuacion = 100

        return {
            "compatible": True,
            "razon": f"RAM suficiente ({ram_disponible}GB disponible, requiere {ram_requerida}GB)",
            "puntuacion": min(puntuacion, 100)
        }

    @classmethod
    def _extraer_gb_ram(cls, texto_ram):
        """Extraer cantidad en GB de texto como '16 GB'"""
        import re
        numeros = re.findall(r'\d+', str(texto_ram))
        if numeros:
            cantidad = int(numeros[0])
            # Si es menor a 100, asumir GB
            if cantidad < 100:
                return cantidad
            else:
                return cantidad // 1024  # Convertir MB a GB
        return 0
    
    @classmethod
    def _calcular_cpu_score(cls, marca, modelo):
        """Calcular puntuación de CPU basada en marca y modelo"""
        marca_lower = marca.lower()
        modelo_lower = modelo.lower()
        
        if marca_lower not in cls.CPU_PERFORMANCE:
            return 50  # Puntuación por defecto
        
        for key, score in cls.CPU_PERFORMANCE[marca_lower].items():
            if key in modelo_lower:
                return score
        
        return 50
    
    @classmethod
    def _calcular_cpu_score_from_string(cls, cpu_string):
        """Calcular puntuación requerida de CPU desde string"""
        cpu_lower = cpu_string.lower()
        
        for marca, series in cls.CPU_PERFORMANCE.items():
            if marca in cpu_lower:
                for key, score in series.items():
                    if key in cpu_lower:
                        return score
        
        return 50
    
    @classmethod
    def _calcular_gpu_score(cls, marca, modelo):
        """Calcular puntuación de GPU basada en marca y modelo"""
        marca_lower = marca.lower()
        modelo_lower = modelo.lower()
        
        if marca_lower not in cls.GPU_PERFORMANCE:
            return 50
        
        for key, score in cls.GPU_PERFORMANCE[marca_lower].items():
            if key in modelo_lower:
                return score
        
        return 50
    
    @classmethod
    def _calcular_gpu_score_from_string(cls, gpu_string):
        """Calcular puntuación requerida de GPU desde string"""
        gpu_lower = gpu_string.lower()
        
        for marca, series in cls.GPU_PERFORMANCE.items():
            if marca in gpu_lower:
                for key, score in series.items():
                    if key in gpu_lower:
                        return score
        
        return 50
    
    @classmethod
    def _generar_recomendaciones(cls, componentes, puntuacion_general):
        """Generar recomendaciones inteligentes basadas en los componentes"""
        recomendaciones = []
        
        if puntuacion_general < 40:
            recomendaciones.append("Tu hardware está por debajo de los requisitos mínimos. Considera actualizar componentes clave.")
        elif puntuacion_general < 60:
            recomendaciones.append("Tu hardware cumple los requisitos mínimos pero podrías experimentar bajo rendimiento.")
        elif puntuacion_general < 80:
            recomendaciones.append("Tu hardware es bueno. Los juegos deberían funcionar bien en configuraciones medias-altas.")
        else:
            recomendaciones.append("¡Excelente hardware! Podrás jugar en configuraciones ultra con buen rendimiento.")
        
        # Verificar balance de componentes
        cpu_componentes = [c for c in componentes if c.tipo == "CPU"]
        gpu_componentes = [c for c in componentes if c.tipo == "GPU"]
        
        if cpu_componentes and gpu_componentes:
            cpu_score = cls._calcular_cpu_score(cpu_componentes[0].marca, cpu_componentes[0].modelo)
            gpu_score = cls._calcular_gpu_score(gpu_componentes[0].marca, gpu_componentes[0].modelo)
            
            if abs(cpu_score - gpu_score) > 20:
                if cpu_score > gpu_score:
                    recomendaciones.append("Tu CPU es más potente que tu GPU. Considera actualizar la GPU para mejor balance.")
                else:
                    recomendaciones.append("Tu GPU es más potente que tu CPU. Considera actualizar el CPU para evitar cuellos de botella.")
        
        return recomendaciones
