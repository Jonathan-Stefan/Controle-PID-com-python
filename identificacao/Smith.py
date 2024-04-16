def Smith(Step, Time, Output):
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
        if Output[i] >= 0.283 * valorFinal and t1 == 0:
            t1 = Time[i]
        
        if Output[i] >= 0.6321 * valorFinal:
            t2 = Time[i]
            break
    
    tau = 1.5 * (t2 - t1)
    Theta = t2 - tau
    identificacaoSmith = [k, tau, Theta]
    
    return identificacaoSmith
