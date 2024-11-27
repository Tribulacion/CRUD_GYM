from conexion import Conexion
from cliente import Cliente
from logger_base import log

class ClienteDAO:
    SELECCIONAR = 'SELECT * FROM cliente ORDER BY Id'
    INSERTAR = 'INSERT INTO cliente(nombre, apellido, membresia) VALUES(%s, %s, %s)'
    ACTUALIZAR = 'UPDATE cliente SET nombre=%s, apellido=%s, membresia=%s WHERE id=%s'
    ELIMINAR = 'DELETE FROM cliente WHERE id=%s'

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            log.debug('Iniciando el método seleccionar')
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            # Mapeo de clase-tabla cliente
            clientes = []
            for registro in registros:
                cliente = Cliente(registro[0], registro[1], registro[2], registro[3])
                clientes.append(cliente)
            log.debug(f'Selección de clientes: {clientes}')
            return clientes
        except Exception as e:
            log.error(f'Ocurrio un error al seleccionar clientes: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                log.debug('Conexión cerrada después de seleccionar')

    @classmethod
    def insertar(cls, cliente):
        log.debug(f'Insertar cliente: {cliente}')
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            # Insertar el valor de membresia como un entero
            valores = (cliente.nombre, cliente.apellido, cliente.membresia)
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            log.debug(f'Cliente insertado: {cliente}')
            return cursor.rowcount
        except Exception as e:
            log.error(f'Ocurrio un error al insertar un cliente: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                log.debug('Conexión cerrada después de insertar')

    @classmethod
    def actualizar(cls, cliente):
        log.debug(f'Actualizar cliente: {cliente}')
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            # Actualizar el cliente
            valores = (cliente.nombre, cliente.apellido, cliente.membresia, cliente.id)
            cursor.execute(cls.ACTUALIZAR, valores)
            conexion.commit()
            log.debug(f'Cliente actualizado: {cliente}')
            return cursor.rowcount
        except Exception as e:
            log.error(f'Ocurrio un error al actualizar un cliente: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                log.debug('Conexión cerrada después de actualizar')

    @classmethod
    def eliminar(cls, cliente):
        log.debug(f'Eliminar cliente: {cliente}')
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.id,)
            cursor.execute(cls.ELIMINAR, valores)
            conexion.commit()
            log.debug(f'Cliente eliminado: {cliente}')
            return cursor.rowcount
        except Exception as e:
            log.error(f'Ocurrio un error al eliminar un cliente: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)
                log.debug('Conexión cerrada después de eliminar')


if __name__ == '__main__':
    # Insertar cliente
    cliente1 = Cliente(nombre='Carlos', apellido='Monroy', membresia=300)
    clientes_insertados = ClienteDAO.insertar(cliente1)
    print(f'Clientes insertados: {clientes_insertados}')

    # Actualizar cliente
    cliente1.nombre = 'Carlos Actualizado'
    clientes_actualizados = ClienteDAO.actualizar(cliente1)
    print(f'Clientes actualizados: {clientes_actualizados}')