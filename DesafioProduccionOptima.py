#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 19:40:28 2020

@author: diegorivera

Desafio Porducción Óptima
"""

import gurobipy as gp

# parametros
# utilidad por litro de cada una de estas cervezas
utilidad = {'cervezaA':2, 'cervezaB':2, 'cervezaC':6, 'cervezaD':10, 
            'cervezaE':10, 'cervezaF':2, 'cervezaG':8}

# capacidad max. en bodega de insumos de cervezas, en kg
capacidad = {'levadura':7000, 'cebada':5000, 'malta':5000, 'trigo':7000,
             'lupulo':2000}

# matriz de produccion
matriz = {}

# datos de composicion de insumos, en kg, para Cerveza tipo "A"
matriz['cervezaA'] = {'levadura':2, 'cebada':1, 'malta':0, 'trigo':7, 
                      'lupulo':2}

# datos de composicion de insumos, en kg, para Cerveza tipo "B"
matriz['cervezaB'] = {'levadura':7, 'cebada':1, 'malta':3, 'trigo':1, 
                      'lupulo':2}

# datos de composicion de insumos, en kg, para Cerveza tipo "C"
matriz['cervezaC'] = {'levadura':1, 'cebada':3, 'malta':1, 'trigo':3, 
                      'lupulo':0}

# datos de composicion de insumos, en kg, para Cerveza tipo "D"
matriz['cervezaD'] = {'levadura':3, 'cebada':5, 'malta':2, 'trigo':9, 
                      'lupulo':4}

# datos de composicion de insumos, en kg, para Cerveza tipo "E"
matriz['cervezaE'] = {'levadura':9, 'cebada':5, 'malta':0, 'trigo':0, 
                      'lupulo':9}

# datos de composicion de insumos, en kg, para Cerveza tipo "F"
matriz['cervezaF'] = {'levadura':0, 'cebada':1, 'malta':0, 'trigo':1, 
                      'lupulo':1}

# datos de composicion de insumos, en kg, para Cerveza tipo "G"
matriz['cervezaG'] = {'levadura':1, 'cebada':4, 'malta':4, 'trigo':6, 
                      'lupulo':2}
# armar modelo
modelo = gp.Model("produccion")

# incorporando variables de decision al modelo
x = {}
for cerveza in utilidad:
    x[cerveza] = modelo.addVar(obj=utilidad[cerveza], lb=0, 
                 vtype=gp.GRB.CONTINUOUS, name='x[%s]'%(cerveza))

# direccion de optimizacion en base a la funcion objetivo, maximizar produccion
# de cerveza
modelo.modelSense = gp.GRB.MAXIMIZE

# incorporando resticciones de capacidad al modelo
for insumo in capacidad:
    # restriccion del insumo cap
    lexp = gp.LinExpr()
    # sumar cada tipo de cerveza para este insumo
    for cerveza in utilidad:
        lexp.addTerms(matriz[cerveza][insumo], x[cerveza])
    # agregar restriccion
    modelo.addConstr(lexp, gp.GRB.LESS_EQUAL, capacidad[insumo],
                     'capacidad[%s]'%(insumo))

# actualizacion de variables y despliegue del modelo
modelo.update()
modelo.display()

# resolver modelo optimizado
modelo.optimize()

# revisar si llegamos o no al optimo
if modelo.status != gp.GRB.status.OPTIMAL:
    print('HOUSTON, No llegamos al óptimo, algo salió mal, damn it!!!')
else:        
# resolviendo bajo distintos algoritmos de gurobi. Desde metodo 0 hasta el 5
        
        metodo = {0: 'primal simplex', 1: 'dual simplex', 2: 'barrier', 
                  3: 'concurrent', 4: 'deterministic concurrent', 
                  5: 'deterministic concurrent simplex'}
        
        # Estableciendo el valor de los parámetro en un nuevo valor.
        # Este método solo afecta la configuración de parámetros para este 
        # modelo. OutputFlag --> Habilita o deshabilita la salida del 
        # solucionador. Establecer OutputFlag en 0 es equivalente a establecer
        # LogFile en "" y LogToConsole en 0.
        modelo.setParam('OutputFlag', False)
        
        for key in metodo:
            # Reininiciando el modelo, eliminando las resultados, variables y 
            # parametros previos
            modelo.reset()
             
            # seleccion del algoritmo para resolver el modelo, que sera iterado
            # desde 1 hasta 5, de acuerdo a cada algoritmo
            modelo.params.method=key
             
            # actualizacion de variables y resolucion optimizada del modelo
            modelo.update()
            modelo.optimize()
            
            # display de resultados para todos los metodos
            print('-'*80)
            print('Para algoritmo - %s'%(metodo[key]),'. Con metodo = ',key)
            print('\nValor optimo (Utilidad): %.2f\n'%(modelo.ObjVal))
            
            # Valores de las variables de decisiones
            print('Se produce:')
            for cerveza in utilidad:
                print('%.2f litros de %s'%(x[cerveza].x, cerveza))
            print()
                
            # Costos reducidos
            for cerveza in utilidad:
                print('Costo reducido de x[%s]: %.2f'%(cerveza, x[cerveza].RC))
                    
            for cerveza in utilidad:
                print('\nUtilidad de %s: %.2f'%(cerveza, x[cerveza].Obj))
                print('Intervalo de sensibilidad de %s: [%.2f, %.2f]'%(cerveza,
                          x[cerveza].SAObjLow, x[cerveza].SAObjUp))
            print()
            print(80*'-')    
            print()
                
            # Analisis de sensibilidad
            for insumo in capacidad.keys():
                constraint = modelo.getConstrByName('capacidad[%s]'%(insumo))
                    
                # Imprimir valor holgura
                print('Holgura de capacidad[%s]: %.2f'%(insumo, constraint.Slack))
                    
                # Imprimir valor dual
                print('Valor dual de capacidad[%s]: %.2f'%(insumo, constraint.Pi))
                    
                # Imprinir valor actual del lado derecha de la restriccion
                print('Valor actual RHS en %s: %.2f'%(insumo, constraint.RHS))
                    
                # Imprimir intervalo de sensibilidad, capacidad por insumox
                print('Intervalo de sensibilidad de capacidad[%s]: [%.2f, %.2f]'
                      %(insumo, constraint.SARHSLow, constraint.SARHSUp))
                print()
                print(80*'-')  
                