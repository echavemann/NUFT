// Package declaration
package main

// Importing packages

type tuple struct {
	price    float64
	buy_sell bool
}

func GGM(stock_price float64, dividends_per_share float64, required_rate_return float64, dividend_growth_rate float64) tuple {
	var expected_stock_price float64 = dividends_per_share / (required_rate_return - dividend_growth_rate)
	var buy_sell bool = stock_price < expected_stock_price // buy - 1 , sell - 0
	output := tuple{expected_stock_price, buy_sell}
	return output
}
