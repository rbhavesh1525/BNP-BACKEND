from Models.linear_regression_model import predict_portfolio

def generate_portfolio_service(data):
    """
    Uses the linear regression ML model to predict portfolio returns.
    """
    input_data = {
        "investment_amount": data.investment_amount,
        "tenure": data.tenure,
        "risk_profile": data.risk_profile,
        "investment_type": data.investment_type or "general"
    }

    # Predict
    model_result = predict_portfolio(input_data)
    expected_return = model_result["prediction"]

    projected_growth = round(
        data.investment_amount * ((1 + expected_return) ** data.tenure), 2
    )

    return {
        "user_input": input_data,
        "model_output": {
            "expected_return": expected_return,
            "projected_growth": projected_growth,
            "message": f"Predicted portfolio growth for {data.risk_profile} risk profile"
        }
    }
