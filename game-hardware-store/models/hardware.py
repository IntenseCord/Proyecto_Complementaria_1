class Hardware:
    """Modelo para componentes de hardware"""

    def __init__(self, id, tipo, marca, modelo, precio, descripcion, imagen, especificaciones):
        self.id = id
        self.tipo = tipo  # CPU, GPU, RAM, Motherboard, etc.
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.descripcion = descripcion
        self.imagen = imagen
        self.especificaciones = especificaciones  # dict con detalles técnicos

    @classmethod
    def get_all_hardware(cls):
        """Obtener todo el hardware disponible"""
        hardware = [
            # CPUs
            Hardware(
                id=1,
                tipo="CPU",
                marca="Intel",
                modelo="Core i5-12400F",
                precio=199.99,
                descripcion="Procesador de 12ª generación para gaming",
                imagen="/static/images/i5-12400f.jpg",
                especificaciones={
                    "nucleos": 6,
                    "hilos": 12,
                    "frecuencia_base": "2.5 GHz",
                    "frecuencia_boost": "4.4 GHz",
                    "socket": "LGA 1700",
                    "tdp": "65W"
                }
            ),
            Hardware(
                id=2,
                tipo="CPU",
                marca="AMD",
                modelo="Ryzen 5 7600X",
                precio=299.99,
                descripcion="Procesador Zen 4 para alto rendimiento",
                imagen="/static/images/r5-7600x.jpg",
                especificaciones={
                    "nucleos": 6,
                    "hilos": 12,
                    "frecuencia_base": "4.7 GHz",
                    "frecuencia_boost": "5.3 GHz",
                    "socket": "AM5",
                    "tdp": "105W"
                }
            ),
            # GPUs
            Hardware(
                id=3,
                tipo="GPU",
                marca="NVIDIA",
                modelo="RTX 4060",
                precio=399.99,
                descripcion="Tarjeta gráfica con Ray Tracing",
                imagen="/static/images/rtx4060.jpg",
                especificaciones={
                    "memoria": "8 GB GDDR6",
                    "consumo": "115W",
                    "puertos": "HDMI, DisplayPort x3"
                }
            ),
            Hardware(
                id=4,
                tipo="GPU",
                marca="AMD",
                modelo="RX 7600",
                precio=349.99,
                descripcion="Radeon con arquitectura RDNA 3",
                imagen="/static/images/rx7600.jpg",
                especificaciones={
                    "memoria": "8 GB GDDR6",
                    "consumo": "165W",
                    "puertos": "HDMI, DisplayPort x3"
                }
            ),
            # RAM
            Hardware(
                id=5,
                tipo="RAM",
                marca="Corsair",
                modelo="Vengeance LPX 16GB DDR4",
                precio=89.99,
                descripcion="Memoria de alto rendimiento para gaming",
                imagen="/static/images/ram16gb.jpg",
                especificaciones={
                    "capacidad": "16 GB",
                    "tipo": "DDR4",
                    "frecuencia": "3200 MHz",
                    "latencia": "CL16"
                }
            ),
            Hardware(
                id=6,
                tipo="RAM",
                marca="G.Skill",
                modelo="Trident Z RGB 32GB DDR4",
                precio=159.99,
                descripcion="Memoria RGB premium para entusiastas",
                imagen="/static/images/ram32gb.jpg",
                especificaciones={
                    "capacidad": "32 GB",
                    "tipo": "DDR4",
                    "frecuencia": "3600 MHz",
                    "latencia": "CL18"
                }
            ),
            # Motherboards
            Hardware(
                id=7,
                tipo="Motherboard",
                marca="ASUS",
                modelo="ROG Strix B450-F Gaming",
                precio=129.99,
                descripcion="Placa base ATX para AMD",
                imagen="/static/images/b450.jpg",
                especificaciones={
                    "socket": "AM4",
                    "formato": "ATX",
                    "slots_ram": 4,
                    "slots_pcie": "2 x PCIe 3.0 x16"
                }
            ),
            Hardware(
                id=8,
                tipo="Motherboard",
                marca="MSI",
                modelo="MAG B660M Mortar WiFi",
                precio=149.99,
                descripcion="Placa base micro-ATX para Intel",
                imagen="/static/images/b660m.jpg",
                especificaciones={
                    "socket": "LGA 1700",
                    "formato": "Micro-ATX",
                    "slots_ram": 4,
                    "slots_pcie": "1 x PCIe 4.0 x16"
                }
            )
        ]
        return hardware

    @classmethod
    def get_hardware_by_tipo(cls, tipo):
        """Obtener hardware por tipo"""
        hardware = cls.get_all_hardware()
        return [item for item in hardware if item.tipo.lower() == tipo.lower()]

    @classmethod
    def get_hardware_by_id(cls, hardware_id):
        """Obtener hardware por ID"""
        hardware = cls.get_all_hardware()
        return next((item for item in hardware if item.id == hardware_id), None)

    @classmethod
    def buscar_hardware(cls, consulta):
        """Buscar hardware por marca, modelo o descripción"""
        hardware = cls.get_all_hardware()
        consulta_lower = consulta.lower()
        return [item for item in hardware
                if (consulta_lower in item.marca.lower() or
                    consulta_lower in item.modelo.lower() or
                    consulta_lower in item.descripcion.lower())]
