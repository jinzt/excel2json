--[[
lua配置表 Ratio:表示倍率
]]--
return {
	[1] = 
	{
		TaxRatio = 
		{
			Base = 1000,
			Ratio = 1
		},
		Reward = {
			[1] = 2,[2] = 3,[3] = 4
		},
		Ratio = nil,
		ID = 100
	},[2] = 
	{
		TaxRatio = 
		{
			Base = nil,
			Ratio = 1
		},
		Reward = nil,
		Ratio = 0.7,
		ID = 101
	}
}