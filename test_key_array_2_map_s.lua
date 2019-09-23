--[[
lua配置表 Ratio:表示倍率
]]--
return {
	["102"] = 
	{
		["TaxRatio"] = 
		{
			["Base"] = 1000,
			["Ratio"] = 1
		},
		["Reward"] = {
			[1] = 10,[2] = 15,[3] = 20
		},
		["Ratio"] = 0.5,
		["ID"] = 102
	},
	["103"] = 
	{
		["TaxRatio"] = 
		{
			["Base"] = nil,
			["Ratio"] = 1
		},
		["Reward"] = {
			[1] = 10,[2] = 15,[3] = 20
		},
		["Ratio"] = 0.8,
		["ID"] = 103
	},
	["100"] = 
	{
		["TaxRatio"] = 
		{
			["Base"] = 1000,
			["Ratio"] = 1
		},
		["Reward"] = {
			[1] = 2,[2] = 3,[3] = 4
		},
		["Ratio"] = nil,
		["ID"] = 100
	},
	["101"] = 
	{
		["TaxRatio"] = 
		{
			["Base"] = nil,
			["Ratio"] = 1
		},
		["Reward"] = nil,
		["Ratio"] = 0.7,
		["ID"] = 101
	}
}