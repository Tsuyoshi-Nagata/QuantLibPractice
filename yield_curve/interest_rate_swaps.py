# construct discount curve and libor curve
import QuantLib as ql


risk_free_rate = 0.01
libor_rate = 0.02
day_count = ql.Actual365Fixed()



#追加
calculation_date = ql.Date(20, 10, 2015)

discount_curve = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, risk_free_rate, day_count)
)

libor_curve = ql.YieldTermStructureHandle(
    ql.FlatForward(calculation_date, libor_rate, day_count)
)
#libor3M_index = ql.Euribor3M(libor_curve)  
libor3M_index = ql.USDLibor(ql.Period(3, ql.Months), libor_curve)



"""
スワップ金利商品を構築するためには
固定金利部分と変動金利部分を決める必要がある
"""

calendar = ql.UnitedStates()
settle_date = calendar.advance(calculation_date, 5, ql.Days)
maturity_date = calendar.advance(settle_date, 10, ql.Years)

#固定金利期間とそのスケジュール
fixed_leg_tenor = ql.Period(6, ql.Months)
fixed_schedule = ql.Schedule(settle_date, maturity_date, 
                             fixed_leg_tenor, calendar,
                             ql.ModifiedFollowing, ql.ModifiedFollowing,
                             ql.DateGeneration.Forward, False)

#変動金利期間とそのスケジュール
float_leg_tenor = ql.Period(3, ql.Months)
float_schedule = ql.Schedule (settle_date, maturity_date, 
                              float_leg_tenor, calendar,
                              ql.ModifiedFollowing, ql.ModifiedFollowing,
                              ql.DateGeneration.Forward, False)



#バニラスワップの構築

notional = 10000000
fixed_rate = 0.025
fixed_leg_daycount = ql.Actual360()
float_spread = 0.004
float_leg_daycount = ql.Actual360()

ir_swap = ql.VanillaSwap(ql.VanillaSwap.Payer, notional, fixed_schedule, 
               fixed_rate, fixed_leg_daycount, float_schedule,
               libor3M_index, float_spread, float_leg_daycount )


swap_engine = ql.DiscountingSwapEngine(discount_curve)
ir_swap.setPricingEngine(swap_engine)


#固定金利のキャッシュフロー
for i, cf in enumerate(ir_swap.leg(0)):
    print ("%2d    %-18s  %10.2f"%(i+1, cf.date(), cf.amount()))


#変動金利のキャッシュフロー
for i, cf in enumerate(ir_swap.leg(1)):
    print ("%2d    %-18s  %10.2f"%(i+1, cf.date(), cf.amount()))