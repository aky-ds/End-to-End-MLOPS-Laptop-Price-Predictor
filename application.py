from flask import Flask, request, render_template
from src.Pipeline.Prediction_pipeline import Prediction,Custom_Data
application = Flask(__name__)
app=application
@app.route("/predict", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("index.html")
    else:
        try:
            brand = request.form.get("brand")
            processor_brand = request.form.get("processor_brand")
            processor_name = request.form.get("processor_name")
            processor_gnrtn = float(request.form.get("processor_gnrtn"))
            ram_gb = float(request.form.get("ram_gb"))
            ram_type = request.form.get("ram_type")
            ssd = float(request.form.get("ssd"))
            hdd = float(request.form.get("hdd"))
            os = request.form.get("os")
            os_bit = request.form.get("os_bit")
            graphic_card_gb = float(request.form.get("graphic_card_gb"))
            weight = request.form.get("weight")
            warranty = float(request.form.get("warranty"))
            Touchscreen = request.form.get("Touchscreen")
            msoffice = request.form.get("msoffice")
            rating = float(request.form.get("rating"))
            Number_of_Ratings = float(request.form.get("Number of Ratings"))
            Number_of_Reviews = float(request.form.get("Number of Reviews"))

            data = Custom_Data(
                brand=brand,
                processor_brand=processor_brand,
                processor_name=processor_name,
                processor_gnrtn=processor_gnrtn,
                ram_gb=ram_gb,
                ram_type=ram_type,
                ssd=ssd,
                hdd=hdd,
                os=os,
                os_bit=os_bit,
                graphic_card_gb=graphic_card_gb,
                weight=weight,
                warranty=warranty,
                Touchscreen=Touchscreen,
                msoffice=msoffice,
                rating=rating,
                Number_of_Ratings=Number_of_Ratings,
                Number_of_Reviews=Number_of_Reviews,
            )
            final_data = data.get_data_as_dataframe()

            predict_pipeline = Prediction()
            pred = predict_pipeline.predict(final_data)
            result = round(pred[0], 2)

            return render_template("result.html", final_result=result)
        except ValueError:
            # Handle conversion errors gracefully
            return render_template("error.html", error_message="Please enter valid numerical values for all fields.")

if __name__ == "__main__":
    app.run(host="0.0.0.0")