import numpy as np
import pandas as pd

from data.test_api import evaluate
from data_utils import read_image

forward = lambda x: x

def replace_feature_number(x, validation_sample_size):
    if x==validation_sample_size:
        return "All"
    elif x>validation_sample_size:
        raise ValueError(f"More samples ({x}) than expected maximum ({validation_sample_size})")
    else:
        return x

num_elem_from_repr = lambda x: len(x.split(","))

def download_prediction(name, wandb_run):
    label_artifact = wandb_run.use_artifact("nicojahn/htcv/final_prediction:" + name, type="predictions")
    path = label_artifact.get_path("final_prediction.tif")
    downloaded_prediction = path.download(f"archive/{wandb_run.name}/{name}/")
    return downloaded_prediction

def get_models(selected_models, wandb_run):
    new_dict = {}
    for index, row in selected_models.iterrows():
        tmp_dict = {}
        path = download_prediction(row["name"], wandb_run)
        predictions = read_image(path, scale=False)
        acc, class_acc, kappa = evaluate(predictions)

        tmp_dict["nb_pru"] = row["nb_pru"]
        tmp_dict["models"] = row["models"]
        tmp_dict["lambda"] = row["lambda"]
        tmp_dict["data_set_size"] = row["data_set_size"]
        tmp_dict["m"] = row["m"]

        tmp_dict["time"] = row["time"]
        tmp_dict["test_accuracy"] = acc
        tmp_dict["test_class_accuracies"] = repr(class_acc)
        tmp_dict["test_balanced_accuracy"] = np.mean(class_acc)
        tmp_dict["test_kappa"] = kappa

        new_dict[row["name"]] = tmp_dict

    return pd.DataFrame.from_dict(new_dict).T.astype({"time":float, "test_accuracy":float, \
                                                  "test_class_accuracies":str, "test_balanced_accuracy":float, \
                                                  "test_kappa":float, "m":int, "data_set_size":int, \
                                                  "nb_pru":int, "models":str})

def get_results_formatted(df, column_name, group_by, lambda_func=forward):
    df_ = df.reset_index()[["nb_pru", "test_accuracy", "index", "data_set_size", "models","time"]]\
                .rename(columns={"nb_pru":"remaining", "test_accuracy":"accuracy"})
    
    df_["values"] = df_[["remaining", "accuracy", "time"]]\
                        .agg(lambda x: {"remaining":x[0], "accuracy":x[1], "time":x[2]}, axis=1) 
    df_ = pd.pivot_table(df_, columns=[group_by, "index"], values=["values"], aggfunc=lambda x:x)
    df_ = list(df_.T.groupby(by=group_by, as_index=True, sort=False).agg(lambda x: list(x)).to_dict()["values"].items())

    return [{column_name: lambda_func(elem[0]), "scores":elem[1]} for elem in df_]

def print_latex_friendy(z):
    if "accuracy" in z:
        a = z["accuracy"][["mean", "std"]].agg(lambda xxx: f"{xxx[0]*100:.1f}" + " pm " + f"{xxx[1]*100:.1f}", axis=1)
        del z["accuracy"]
        z["accuracy"] = a

    if "time" in z:
        t = z["time"][["mean", "std"]].agg(lambda xxx: f"{xxx[0]:.1f}" + " pm " + f"{xxx[1]:.1f}", axis=1)
        del z["time"]
        z["time"] = t
    
    if "name" in z:
        c = z["name"]
        del z["name"]
        #z["count"] = c

    z.reset_index(level=0, inplace=True)
    print("\\tn\n".join([y for y in "".join(z.to_latex(index=False, escape=False)\
                                            .split("\\")).split("\n") if "&" in y])\
                      .replace("pm", "$\\pm$") + "\\tn")
    
def get_data(sweeps, runs):
    data_list = []
    for run in runs: 
        # .summary contains the output keys/values for metrics like accuracy.
        #  We call ._json_dict to omit large files
        if not run.sweepName:
            continue
        elif not "finished" in run.state:
            continue
        elif not "time" in run.summary._json_dict:
            continue
        elif run.summary._json_dict["time"] > run.config["timeout"]:
            continue

        is_desired_sweep = False
        for sweep in sweeps:
            if sweep in run.sweepName:
                is_desired_sweep = True
                break        
        if not is_desired_sweep:
            continue
        # .config contains the hyperparameters.
        #  We remove special values that start with _.
        config_dict = {k: v for k,v in run.config.items() if not k.startswith('_')}

        d = {}
        d["name"] = run.name
        for k in ["lambda", "nb_pru", "models", "data_set_size", "m"]:
            d[k] = config_dict[k]
        for k in ["accuracy", "time"]:
            d[k] = run.summary._json_dict[k]
        data_list.append(d)
    x = pd.DataFrame.from_dict(data_list)
    x["models"] = x["models"].aggregate(lambda y: ",".join(y))
    return x