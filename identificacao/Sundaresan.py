def Sundaresan(Step, Time, Output):
    if not isinstance(Time, list) or not isinstance(Output, list) or len(Time) < 1 or len(Output) < 1:
        raise TypeError('Type Error: The arguments must be non-empty lists.')
        
    if not isinstance(Step, (int, float)):
        raise TypeError('TypeError: The argument \'Step\' must be a constant.')
    
    Output = [x - Output[0] for x in Output]
    valorFinal = Output[-1]
    k = valorFinal / Step
    
    t1 = 0
    t2 = 0
    for i in range(len(Output)):
        if Output[i] >= 0.353 * valorFinal and t1 == 0:
            t1 = Time[i]
        
        if Output[i] >= 0.853 * valorFinal:
            t2 = Time[i]
            break
    
    tau = 2 / 3 * (t2 - t1)
    Theta = 1.3 * t1 - 0.29 * t2
    identificacaoSundaresan = [k, tau, Theta]
    
    return identificacaoSundaresan
