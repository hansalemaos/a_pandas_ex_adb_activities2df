import os
import subprocess
import sys
from typing import Union

import pandas as pd
import regex
from a_pandas_ex_plode_tool import qq_s_isnan
from flatten_everything import flatten_everything
from a_pandas_ex_xml2df import xml_to_df
from subprocess_print_and_capture import (
    execute_subprocess_multiple_commands_with_timeout_bin,
)



def execute_multicommands_adb_shell(
    adb_path,
    device_serial,
    subcommands: list,
    exit_keys: str = "ctrl+x",
    print_output=True,
    timeout=None,
):
    if not isinstance(subcommands, list):
        subcommands = [subcommands]
    return execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=f"{adb_path} -s {device_serial} shell",
        subcommands=subcommands,
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )


def execute_command_adb(adb_path, device_serial, command: str):
    proc = subprocess.run(
        f"{adb_path} -s {device_serial} {command}", capture_output=True
    )
    return (
        proc.stdout.decode("utf-8", "ignore"),
        proc.stderr.decode("utf-8", "ignore"),
        proc.returncode,
    )


def connect_to_adb(adb_path: str, deviceserial: str) -> None:
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    _ = subprocess.run(
        f"{adb_path} connect {deviceserial}", capture_output=True, shell=False
    )


def pull(adb_path, deviceserial, path_pc, sd_card_path="/sdcard/"):
    path_pc = os.path.normpath(path_pc)

    if not os.path.exists(path_pc):
        os.makedirs(path_pc)
    execu = fr"pull {sd_card_path} {path_pc}"
    return execute_command_adb(adb_path, deviceserial, execu)


def get_package_path_df(adb_path, deviceserial):
    muc = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=["pm list packages -f"],
        exit_keys="ctrl+x",
        print_output=True,
    )
    muc = [x.decode("utf-8", "replace") for x in muc]
    df = pd.DataFrame(
        [[y.strip() for y in regex.split(r"[:=]+", x)[1:]] for x in muc]
    ).rename(columns={0: "package_path", 1: "package_name"})
    return df


def get_package_infos(
    adb_path, deviceserial, package, tmp_folder_hdd, androguard_cli_py
):

    downloadedpackage = package.split("/")[-1]
    downloadedpackagepath = os.path.normpath(
        os.path.join(tmp_folder_hdd, downloadedpackage)
    )
    pull(adb_path, deviceserial, tmp_folder_hdd, f"{package}")

    outputfile = "".join(downloadedpackagepath.split(".")[:-1]) + ".xml"
    subprocess.run(
        [
            sys.executable,
            androguard_cli_py,
            "axml",
            downloadedpackagepath,
            "-o",
            outputfile,
        ]
    )
    with open(outputfile, encoding="utf-8") as f:
        data = f.read()
    return data


def list_all_packages(adb_path: str, deviceserial: str,) -> pd.DataFrame:
    df = get_package_path_df(adb_path, deviceserial)
    return df


def get_package_infos_df(
    dframe: Union[None, pd.DataFrame],
    adb_path: str,
    deviceserial: str,
    tmp_folder_hdd: str,
    androguard_cli_py: str,
    explode_name_columns: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:

    if isinstance(dframe, type(None)):
        dframe = list_all_packages(adb_path, deviceserial)
    df = dframe.copy()
    df["package_xml"] = df["package_path"].apply(
        lambda x: get_package_infos(
            adb_path=adb_path,
            deviceserial=deviceserial,
            package=x,
            tmp_folder_hdd=tmp_folder_hdd,
            androguard_cli_py=androguard_cli_py,
        )
    )

    alldfs = []
    otherinfos = []

    for key1, item1 in df.iterrows():
        dfn = xml_to_df(item1.package_xml).reset_index()
        for name, group in dfn.groupby(["level_0"], dropna=False):
            for name2, group2 in group.groupby("level_1", dropna=False):
                if (
                    group2.level_1.iloc[0] == "activity"
                    or group2.level_1.iloc[0] == "activity-alias"
                ):
                    for name3, group3 in group2.groupby("level_2", dropna=False):
                        gr = group3[["aa_all_keys", "aa_value"]]
                        newdf = gr.copy()
                        try:
                            newdf["aa_all_keys"] = newdf["aa_all_keys"].apply(
                                lambda x: x[-1].split("}")[-1]
                                if isinstance(x[-1], str)
                                else str(x[-2]).split("}")[-1]
                            )
                        except Exception:
                            newdf["aa_all_keys"] = newdf["aa_all_keys"].apply(
                                lambda x: str(x)
                            )
                        newdf = newdf.groupby("aa_all_keys", as_index=False).agg(
                            {
                                "aa_value": lambda x: x,
                                "aa_all_keys": lambda x: [
                                    f"{y}_{ini}" for ini, y in enumerate(x)
                                ],
                            }
                        )
                        keys = list(flatten_everything(newdf.aa_all_keys.to_list()))
                        values = list(flatten_everything(newdf.aa_value.to_list()))
                        dfnas = (
                            pd.DataFrame(list(zip(keys, values))).set_index(0).T.copy()
                        ).copy()
                        dfnas["aa_package_path"] = item1["package_path"]
                        dfnas["aa_package_name"] = item1["package_name"]
                        dfnas = dfnas.filter(list(sorted(dfnas.columns)))
                        if group2.level_1.iloc[0] == "activity-alias":
                            dfnas["is_alias"] = True
                        else:
                            dfnas["is_alias"] = False

                        alldfs.append(dfnas.copy())
                else:
                    group432 = group2.copy()
                    group432["aa_package_path"] = item1["package_path"]
                    group432["aa_package_name"] = item1["package_name"]
                    otherinfos.append(group432.copy())
    dfa1 = pd.concat(alldfs)

    dft = dfa1.copy()
    if explode_name_columns:
        dft.loc[:, "aa_activity_name"] = tuple(
            tuple(set(z for z in flatten_everything(y) if not qq_s_isnan(z)))
            for y in (
                zip(
                    dft[
                        [x for x in dft.columns if str(x).startswith("name_")]
                    ].__array__()
                )
            )
        )
        dft = dft.explode("aa_activity_name")
    dft.columns = [f"aa_{x}" if str(x).startswith("name_") else x for x in dft.columns]
    dft = dft.filter(list(sorted(dft.columns))).reset_index(drop=True)
    return dft, pd.concat(otherinfos.copy(), ignore_index=True)
