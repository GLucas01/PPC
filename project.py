def sum_a_f(a,f,i) :
    sum=0
    for x in range(i+1):
        sum+=a[x]*f[x]
    return sum
    
    
def sum_B_u(B,u,i) :
    sum=0
    for x in range(i+1):
        sum+=B[x]*u[x]
    return sum
    
    
a=[0.001]
f=[1/5]
B=[0.01]
u=[1]
y=0.99
Pt_1=0.145


Pt = (y*Pt_1)+sum_a_f(a,f,0)+sum_B_u(B,u,0)




print("Pt : "+str(Pt))

