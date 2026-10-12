def generate_insights(df):

    insights = []

    # Khu vực tốt nhất
    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = region_profit.index[0]

    insights.append(
        f"🏆 {best_region} là khu vực mang lại lợi nhuận cao nhất."
    )

    # Khu vực kém nhất
    worst_region = region_profit.index[-1]

    insights.append(
        f"⚠️ {worst_region} là khu vực có lợi nhuận thấp nhất."
    )

    # Danh mục tốt nhất
    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_category = category_profit.index[0]

    insights.append(
        f"📈 {best_category} là danh mục tạo ra lợi nhuận cao nhất."
    )

    # Sản phẩm thua lỗ
    loss_products = (
        df.groupby("Product Name")["Profit"]
        .sum()
    )

    negative_count = (
        loss_products < 0
    ).sum()

    insights.append(
        f"❌ Có {negative_count} sản phẩm đang kinh doanh thua lỗ."
    )

    return insights

def generate_recommendations(df):

    recommendations = []

    negative_products = (
        df.groupby("Product Name")["Profit"]
        .sum()
    )

    loss_count = (
        negative_products < 0
    ).sum()

    if loss_count > 0:

        recommendations.append(
            f"⚠️ Có {loss_count} sản phẩm không sinh lời. Hãy xem xét lại chính sách giá hoặc mức chiết khấu."
        )

    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = region_profit.index[0]

    recommendations.append(
        f"🚀 Tăng cường đầu tư vào {best_region}, đây là khu vực có lợi nhuận tốt nhất."
    )

    return recommendations