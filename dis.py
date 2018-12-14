from openmdao.api import ExplicitComponent
import math
import numpy as np



class Xcomp(ExplicitComponent):

    def initialize(self):
        self.options.declare('num', default=1, types=int)


    def setup(self):
        #input
        self.add_input('q',shape=(num,2))
        self.add_input('L_1',val=0.3)
        self.add_input('L_2',val=0.542)

        #output
        self.add_output('x')
        self.add_output('y')

        #partials
        self.declare_partials('x',['L_1','L_2','q'])
        self.declare_partials('x',['L_1','L_2','q'])

    def compute(self,inputs,outputs):

        L_1=inputs['L_1']
        L_2=inputs['L_2']
        q_1=inputs['q'][0]
        q_2=inputs['q'][1]

        outputs['x']=(L_1)*np.cos(q_1)+(L_2)*np.cos(q_2)
        outputs['y']=(L_1)*np.sin(q_1)+(L_2)*np.sin(q_2)

    def compute_partials(self,inputs,J):

        L_1=inputs['L_1']
        L_2=inputs['L_2']
        q_1=inputs['q'][0]
        q_2=inputs['q'][1]

        J['x','L_1']=np.cos(q_1)
        J['x','L_2']=np.cos(q_2)
        J['x','q_1']=-L_1*np.sin(q_1)
        J['x','q_2']=-L_2*np.sin(q_2)
        J['y','L_1']=np.sin(q_1)
        J['y','L_2']=np.sin(q_2)
        J['y','q_1']=L_1*np.cos(q_1)
        J['y','q_2']=L_2*np.cos(q_2)


if __name__ == '__main__':
    from openmdao.api import Problem, IndepVarComp
    
    num = 20
    
    prob = Problem()
    
    comp = IndepVarComp()
    comp.add_output('L_1',val=0.3)
    comp.add_output('L_2',val=0.542)
    comp.add_output('q',val=np.random.random(num,2))

    prob.model.add_subsystem('ivc', comp, promotes=['*'])
    
    comp = Xcomp(num=num)
    prob.model.add_subsystem('Xcomp', comp, promotes=['*'])
    
    prob.setup()
    
    prob.run_model()
    
    print(prob['x'])
    print(prob['y'])
    
    prob.check_partials(compact_print=True)

