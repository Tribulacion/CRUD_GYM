class Cliente:
    def __init__(self, id=None, nombre=None, apellido=None, membresia=None):
        self._id = id
        self._nombre = nombre
        self._apellido = apellido
        self._membresia = membresia
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre
    
    @property
    def apellido(self):
        return self._apellido
    
    @apellido.setter
    def apellido(self, apellido):
        self._apellido = apellido
    
    @property
    def membresia(self):
        return self._membresia
    
    @membresia.setter
    def membresia(self, membresia):
        self._membresia = membresia

    def __str__(self):
        return (f'Id: {self.id}, Nombre: {self.nombre}, '
                f'Apellido: {self.apellido}, Membresia: {self.membresia}')
