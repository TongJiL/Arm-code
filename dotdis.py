from openmdao.api import ExplicitComponent
import math
import numpy as np



class dotXcomp(ExplicitComponent):

    def initialize(self):
        self.options.declare('num', default=1, types=int)


    def setup(self):
        #input
        self.add_input('q',shape=(num,2))
        self.add_input('w',shape=(num,2))
        self.add_input('L_1',val=0.3)
        self.add_input('L_2',val=0.542)

        #output
        self.add_output('dotx')
        self.add_output('doty')

        #partials
        self.declare_partials('dotx',['L_1','L_2','q','w'])
        self.declare_partials('doty',['L_1','L_2','q','w'])

    def compute(self,inputs,outputs):

        L_1=inputs['L_1']
        L_2=inputs['L_2']
        q_1=inputs['q'][0]
        q_2=inputs['q'][1]
        w_1=inputs['w'][0]
        w_2=inputs['w'][1]

        outputs['dotx']=-(L_1)*(w_1)*np.sin(q_1)-(L_2)*(w_2)*np.sin(q_2)
        outputs['doty']=(L_1)*(w_1)*np.cos(q_1)+(L_2)*(w_2)*np.cos(q_2)

    def compute_partials(self,inputs,J):

        L_1=inputs['L_1']
        L_2=inputs['L_2']
        q_1=inputs['q'][0]
        q_2=inputs['q'][1]
        w_1=inputs['w'][0]
        w_2=inputs['w'][1]


        J['dotx','L_1']=-(w_1)*np.sin(q_1)
        J['dotx','L_2']=-(w_2)*np.sin(q_2)
        J['dotx','q_1']=-(L_1)*(w_1)*np.cos(q_1)
        J['dotx','q_2']=-(L_2)*(w_2)*np.cos(q_2)
        J['dotx','w_1']=-(L_1)*np.sin(q_1)
        J['dotx','w_2']=-(L_2)*np.sin(q_2)
        J['doty','L_1']=(w_1)*np.cos(q_1)
        J['doty','L_2']=-(w_2)*np.cos(q_2)
        J['doty','q_1']=(L_1)*(w_1)*np.sin(q_1)
        J['doty','q_2']=(L_2)*(w_2)*np.sin(q_2)
        J['doty','w_1']=(L_1)*np.cos(q_1)
        J['doty','w_2']=(L_2)*np.cos(q_2)


if __name__ == '__main__':
    from openmdao.api import Problem, IndepVarComp
    
    num = 20
    
    prob = Problem()
    
    comp = IndepVarComp()
    comp.add_output('L_1',val=0.3)
    comp.add_output('L_2',val=0.542)
    comp.add_output('q',val=np.random.random(num,2))
    comp.add_output('w',val=np.random.random(num,2))

    prob.model.add_subsystem('ivc', comp, promotes=['*'])
    
    comp = dotXcomp(num=num)
    prob.model.add_subsystem('dotXcomp', comp, promotes=['*'])
    
    prob.setup()
    
    prob.run_model()
    
    print(prob['dotx'])
    print(prob['doty'])
    
    prob.check_partials(compact_print=True)

