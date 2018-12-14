from openmdao.api import ExplicitComponent
import math
import numpy as np

class Combinedpara(ExplicitComponent):
    #compute the combined model parameters P1-P5.
    def setup(self):
        
        self.add_input('L_1',val=0.3)
        self.add_input('L_2',val=0.542)
        self.add_input('m_1',val=2.934)
        self.add_input('m_2',val=1.1022)
        self.add_input('l_1c',val=0.2071)
        self.add_input('l_2c',val=0.2717)
        self.add_input('I_1',val=0.2067)
        self.add_input('I_2',val=0.1362)
        self.add_input('m_B',val=0.064)
        # outputs
        self.add_output('p_1',0.0)
        self.add_output('p_2',0.0)
        self.add_output('p_3',0.0)
        self.add_output('p_4',0.0)
        self.add_output('p_5',0.0)
        
        #partials
        self.declare_partials('p_1',['L_1','m_B','m_2','I_1'])
        self.declare_partials('p_2',['L_2','I_2','m_B'])
        self.declare_partials('p_3',['L_1','m_B','m_2','L_2','l_2c'])
        self.declare_partials('p_4',['L_1','m_B','m_2','m_1','l_1c'])
        self.declare_partials('p_5',['L_2','m_B','m_2','l_2c'])

    def compute(self,inputs,outputs):
        
        L_1=inputs['L_1']
        L_2=inputs['L_2']
        m_1=inputs['m_1']
        m_2=inputs['m_2']
        l_1c=inputs['l_1c']
        l_2c=inputs['l_2c']
        I_1=inputs['I_1']
        I_2=inputs['I_2']
        m_B=inputs['m_B']
        
        """compute the property of the arm"""
        outputs['p_1']=p_1=(L_1**2)*m_2+(L_1**2)*m_B+I_1
        outputs['p_2']=p_2=(L_2**2)*m_B+I_2
        outputs['p_3']=p_3=L_1*l_2c*m_2+m_B*L_1*L_2
        outputs['p_4']=p_4=m_1*9.81*l_1c+m_2*9.81*L_1+m_B*9.81*L_1
        outputs['p_5']=p_5=m_2*9.81*l_2c+m_B*9.81*L_2
    
    def compute_partials(self,inputs,J):
        
        L_1=inputs['L_1']
        L_2=inputs['L_2']
        m_1=inputs['m_1']
        m_2=inputs['m_2']
        l_1c=inputs['l_1c']
        l_2c=inputs['l_2c']
        I_1=inputs['I_1']
        I_2=inputs['I_2']
        m_B=inputs['m_B']
        
        J['p_1','L_1']=2*m_2*L_1+m_B*2*L_1
        J['p_1','m_B']=L_1**2
        J['p_1','m_2']=L_1**2
        J['p_1','I_1']=1
        J['p_2','L_2']=2*m_B*L_2
        J['p_2','m_B']=L_2**2
        J['p_2','I_2']=1
        J['p_3','L_1']=m_2*l_2c+m_B*L_2
        J['p_3','l_2c']=L_1*m_2
        J['p_3','m_2']=L_1*l_2c
        J['p_3','m_B']=L_1*L_2
        J['p_3','L_2']=L_1*m_B
        J['p_4','m_1']=9.81*l_1c
        J['p_4','l_1c']=9.81*m_1
        J['p_4','m_2']=9.81*L_1
        J['p_4','L_1']=9.81*m_2+9.81*m_B
        J['p_4','m_B']=9.81*L_1
        J['p_5','m_2']=9.81*l_2c
        J['p_5','l_2c']=9.81*m_2
        J['p_5','m_B']=9.81*L_2
        J['p_5','L_2']=9.81*m_B

if __name__ == '__main__':
    from openmdao.api import Problem, IndepVarComp
    
    
    prob = Problem()
    
    comp = IndepVarComp()
    comp.add_output('L_1', val=0.3)
    comp.add_output('L_2', val=0.542)
    comp.add_output('m_1', val=2.934)
    comp.add_output('m_2', val=1.1022)
    comp.add_output('l_1c', val=0.2071)
    comp.add_output('l_2c', val=0.2717)
    comp.add_output('I_1', val=0.2067)
    comp.add_output('I_2', val=0.1362)
    comp.add_output('m_B', val=0.064)

    prob.model.add_subsystem('ivc', comp, promotes=['*'])
    
    comp = Combinedpara()
    prob.model.add_subsystem('Combinedpara', comp, promotes=['*'])
    
    prob.setup()
    
    prob.run_model()
    
    print(prob['p_1'])
    print(prob['p_2'])
    print(prob['p_3'])
    print(prob['p_4'])
    print(prob['p_5'])

    prob.check_partials(compact_print=True)
