from openmdao.api import ExplicitComponent
import math
import numpy as np



class Combinedpara(ExplicitComponent)
#compute the combined model parameters P1-P5.

      def setup(self):
          # inputs
          self.add_input('L_1',val=0.3,units="m",desc="length of the first arm")
          self.add_input('L_2',val=0.542,units="m",desc="length of the second arm")
          self.add_input('m_1',val=2.934,units="kg",desc="Mass of the 1st arm")
          self.add_input('m_2',val=1.1022,units="kg",desc="Mass of the 2nd arm")
          self.add_input('l_1c',val=0.2071,units="m",desc="not sure")
          self.add_input('l_2c',val=0.2717,units="m",desc="not sure")
          self.add_input('I_1',val=0.2067,units="kgm2",desc="moment of inertia of 1st arm")
          self.add_input('I_2',val=0.1362,units="kgm2",desc="Moment of inertia of 2nd arm")
          self.add_input('m_B',val=0.064,desc="mass of the ball")
          self.add_input('g',val=9.81,desc="gravitational constant")
          
          # outputs
          self.add_ouput('p_1',0.0)
          self.add_ouput('p_2',0.0)
          self.add_ouput('p_3',0.0)
          self.add_ouput('p_4',0.0)
          self.add_ouput('p_5',0.0)

          #partials
          self.declare_partials('p_1',['L_1','m_B','m_2','I_1'])
          self.declare_partials('p_2',['L_2','I_2','m_B'])
          self.declare_partials('p_3',['L_1','m_B','m_2','L_2','l_2c'])
          self.declare_partials('p_4',['L_1','m_B','m_2','m_1','g','l_1c'])
          self.declare_partials('p_5',['L_2','m_B','m_2','l_2c','g'])

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
          g=inputs['g']

          """compute the property of the arm"""
          outputs['p_1']=p_1=(L_1**2)*m_2+(L_1**2)*m_B+I_1
          outputs['p_2']=p_2=(L_2**2)*m_B+I_2
          outputs['p_3']=p_3=L_1*l_2c*m_2+m_B*L_1*L_2
          outputs['p_4']=p_4=m_1*g*l_1c+m_2*g*L_1+m_B*g*L_1
          outputs['p_5']=p_5=m_2*g*l_2c+m_B*g*L_2
       
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
          g=inputs['g']
          
          J['p_1','L_1']=2*m_2
          J['p_1','m_B']=L_1**2
          J['p_1','m_2']=L_1**2
          J['p_1','I_1']=1
          J['p_2','L_2']=2*m_B
          J['p_2','m_B']=L_2**2
          J['p_2','I_2']=1
          J['p_3','L_1']=m_2*l_2c+m_B*L_2
          J['p_3','l_2c']=L_1*m_2
          J['p_3','m_2']=L_1*l_2c
          J['p_3','m_B']=L_1*L_2
          J['p_3','L_2']=L_1*m_B
          J['p_4','m_1']=g*l_1c
          J['p_4','g']=m_1*l_1c+m_2*L_1+m_B*L_1
          J['p_4','l_1c']=g*m_1
          J['p_4','m_2']=g*L_1
          J['p_4','L_1']=g*m_2+g*m_B
          J['p_4','m_B']=g*L_1
          J['p_5','m_2']=g*l_2c
          J['p_5','g']=m_2*l_2c+m_B*L_2
          J['p_5','l_2c']=g*m_2
          J['p_5','m_B']=g*L_2
          J['p_5','L_2']=g*m_B


from openmdao.api import Problem
class elements(ExplicitComponent)

      def setup(self)
          #inputs
          self.add_input('k',val=14.1543,units="Nm/rad",desc="spring constant")
          self.add_input('E_k',val=0,desc="offset")
          self.add_input('tor',0.0,desc="torque of the motor")
          self.add_input('q',shape(num,2))
          self.add_input('w',shape(num,2))
          self.add_input('p1')
          self.add_input('p2')
          self.add_input('p3')
          self.add_input('p4')
          self.add_input('p5')
          #outputs
          self.add_output('M_q',shape(num,2,2))
          self.add_output('C_q',shape(num,2,2))
          self.add_output('G_q',shape(num,2))
          self.add_output('K_q',shape(num,2))
          self.add_output('F',shape(num,2))

          #partials
          self.declare_partials('M_q',['p1','p2','p3','q1','q2'])
          self.declare_partials('C_q',['p3','q1','q2','w1','w2'])
          self.declare_partials('G_q',['p4','p5','q1','q2'])
          self.declare_partials('K_q',['k','E_k','q1','q2'])
          self.declare_partials('F',['tor'])

      def compute(self,inputs,outputs)
          """declare inputs"""
          p1=inputs['p1']
          p2=inputs['p2']
          p3=inputs['p3']
          p4=inputs['p4']
          p5=inputs['p5']
          q1=inputs['q']
          q2=inputs['q']
          w1=inputs['w']
          w2=inputs['w']
          k=inputs['k']
          Ek=inputs['E_k']
          tor=inputs['tor']

          outputs['M_q']=np.array[p1,p3*cos(q1-q2)
                                  p3*cos(q1-q2),p2]
          outputs['C_q']=np.array[0,p3*sin(q1-q2)*w2
                                  -p3*sin(q1-q2)*w1,0]
          outputs['G_q']=np.array[p4*cos(q1)
                                  p5*cos(q2)]
          outputs['K_q']=np.array[-k*(q2-q1-Ek)
                                  k*(q2-q1-Ek)]
          outputs['F']=np.array[tor
                                0]

      def compute_partials(self,inputs,J):

          p1=inputs['p1']
          p2=inputs['p2']
          p3=inputs['p3']
          p4=inputs['p4']
          p5=inputs['p5']
          q=inputs['q']
          w=inputs['w']
          k=inputs['k']
          Ek=inputs['E_k']
          tor=inputs['tor']
          
          J['M_q','p1']=np.array[1,0
                                 0,0]
          J['M_q','p2']=np.array[0,0
                                 0,1]
          J['M_q','p3']=np.array[0,cos(q1-q2)
                                 cos(q1-q2),0]
          J['M_q','q1']=np.array[0,-sin(q1-q2)
                                 -sin(q1-q2),0]
          J['M_q','q2']=np.array[0,sin(q1-q2)
                                 sin(q1-q2),0]
          J['C_q','p3']=np.array[0,sin(q1-q2)*w2
                                 -sin(q1-q2)*w1,0]
          J['C_q','q1']=np.array[0,p3*cos(q1-q2)*w2
                                 -p3*cos(q1-q2)*w1,0]
          J['C_q','q2']=np.array[0,-p3*cos(q1-q2)*w2
                                 p3*cos(q1-q2)*w1,0]
          J['C_q','w1']=np.array[0,0
                                 -p3*sin(q1-q2),0]
          J['C_q','w2']=np.array[0,p3*sin(q1-q2)
                                 0,0]
          J['G_q','p4']=np.array[cos(q1)
                                 0]
          J['G_q','p5']=np.array[0
                                 cos(q2)]
          J['G_q','q1']=np.array[-p4*sin(q1)
                                 0]
          J['G_q','q2']=np.array[0
                                 -p5*sin(q2)]
          J['K_q','k']=[q1+Ek-q2
                        q2-q1-Ek]
          J['K_q','E_k']=[k
                          -k]
          J['K_q','q1']=[k
                         -k]
          J['K_q','q2']=[-k
                         k]
          J['F','tor']=[1
                        0]

class component(ExplicitComponent)
#solve for CN_1=inv(M_q)*C_q*w
#CN_2=inv(M_q)*K_q
#CN_3=inv(M_q)*(F-G_q)

      def setup(self)
          #inputs
          self.add_input('M_q',shape(num,2,2))
          self.add_input('C_q',shape(num,2,2))
          self.add_input('G_q',shape(num,2))
          self.add_input('K_q',shape(num,2))
          self.add_input('F',shape(num,2))

          #outputs
          self.add_output('CN_1',shape(num,2))
          self.add_output('CN_2',shape(num,2))
          self.add_output('CN_3',shape(num,2))

          #partials
          self.declare_partials('CN_1',['M_q','C_q','w'])
          self.declare_partials('CN_2',['M_q','K_q'])
          self.declare_partials('CN_1',['M_q','G_q','F'])













self.add_output('tor',0.0,desc="torque of the motor")


                                  
                                  
                                  
                                  comp=IndepVarComp()
                                  
                                  # independent elements
                                  comp.add_input('L_1',val=0.3,units="m",desc="length of the first arm")
                                  comp.add_input('L_2',val=0.542,units="m",desc="length of the second arm")
                                  comp.add_input('m_1',val=2.934,units="kg",desc="Mass of the 1st arm")
                                  comp.add_input('m_2',val=1.1022,units="kg",desc="Mass of the 2nd arm")
                                  comp.add_input('l_1c',val=0.2071,units="m",desc="not sure")
                                  comp.add_input('l_2c',val=0.2717,units="m",desc="not sure")
                                  comp.add_input('I_1',val=0.2067,units="kgm2",desc="moment of inertia of 1st arm")
                                  comp.add_input('I_2',val=0.1362,units="kgm2",desc="Moment of inertia of 2nd arm")
                                  comp.add_input('k',val=14.1543,units="Nm/rad",desc="spring constant")
                                  comp.add_input('E_k',val=0,desc="offset")
                                  comp.add_input('m_B',val=0.064,desc="mass of the ball")
                                  comp.add_input('g',val=9.81,desc="gravitational constant")
