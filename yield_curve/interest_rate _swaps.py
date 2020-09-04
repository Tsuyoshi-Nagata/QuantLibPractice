# construct discount curve and libor curve

risk_free_rate = 0.01
libor_rate = 0.02
day_count = ql.Actual365Fixed()

discount_curve = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, risk_free_rate, day_count)
)

libor_curve = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, libor_rate, day_count)
)
#libor3M_index = ql.Euribor3M(libor_curve)  
libor3M_index = ql.USDLibor(ql.Period(3, ql.Months), libor_curve)