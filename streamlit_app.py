from __future__ import annotations

import pandas as pd
import streamlit as st


PROJECTS = [
    {
        "Customer": "Great Wolf",
        "Region": "NAMER",
        "Implementation Lead": "Nadine Pylypei",
        "Hotels": 24,
        "Channels": "GDS, Booking - Completed, IBE - Completed, Groupon - Completed, Expedia - Completed, Hilton Grand Vacations - Completed, Google / DS META - Completed",
        "Migration Plan": "Jul 1, 2026",
        "Slack": "",
        "Status": "Started",
        "Sort Date": "2026-07-01",
    },
    {
        "Customer": "Minor Hotels",
        "Region": "JAPAC",
        "Implementation Lead": "Hazel Acat",
        "Hotels": 112,
        "Channels": "ORS > OCC Migration, SiteMinder",
        "Migration Plan": "Sep 1, 2026",
        "Slack": "https://oracle.enterprise.slack.com/archives/C08FRQZAFMW",
        "Status": "Scheduled",
        "Sort Date": "2026-09-01",
    },
    {
        "Customer": "Vail Resorts",
        "Region": "NAMER",
        "Implementation Lead": "Colin Determann",
        "Hotels": 62,
        "Channels": "Inntopia, Booking, Expedia, Trip, GDS",
        "Migration Plan": "Pod 1 x 6: Sep 2026 / Pod 2 remaining: Nov 2026",
        "Slack": "https://oracle.enterprise.slack.com/archives/C0AHD3Y0QAW",
        "Status": "Phased",
        "Sort Date": "2026-09-01",
    },
    {
        "Customer": "Voyages",
        "Region": "JAPAC",
        "Implementation Lead": "Anil Vempati",
        "Hotels": 8,
        "Channels": "Booking, Expedia, WebBeds, HotelBeds, JTB Group, Luxury Escapes, Flight Centre, Trip.com",
        "Migration Plan": "Oct 1, 2026",
        "Slack": "",
        "Status": "Scheduled",
        "Sort Date": "2026-10-01",
    },
    {
        "Customer": "Marina Bay Sands",
        "Region": "JAPAC",
        "Implementation Lead": "Nishant Sharma",
        "Hotels": 1,
        "Channels": "TBC",
        "Migration Plan": "Apr 1, 2027",
        "Slack": "",
        "Status": "Channel TBC",
        "Sort Date": "2027-04-01",
    },
    {
        "Customer": "Oceanic",
        "Region": "NAMER",
        "Implementation Lead": "Kurtis Cwiek",
        "Hotels": 15,
        "Channels": "IBE",
        "Migration Plan": "TBC",
        "Slack": "",
        "Status": "Timing TBC",
        "Sort Date": "9999-12-31",
    },
    {
        "Customer": "VAI",
        "Region": "NAMER",
        "Implementation Lead": "Kurtis Cwiek",
        "Hotels": 4,
        "Channels": "Inntopia",
        "Migration Plan": "TBC",
        "Slack": "",
        "Status": "Timing TBC",
        "Sort Date": "9999-12-31",
    },
    {
        "Customer": "Aramark",
        "Region": "NAMER",
        "Implementation Lead": "Kurtis Cwiek",
        "Hotels": 40,
        "Channels": "TBC",
        "Migration Plan": "TBC",
        "Slack": "",
        "Status": "Timing TBC",
        "Sort Date": "9999-12-31",
    },
]

STATUS_COLORS = {
    "Started": "#14928c",
    "Scheduled": "#23a56f",
    "Phased": "#d99822",
    "Channel TBC": "#dc3f46",
    "Timing TBC": "#84766a",
}


def project_frame() -> pd.DataFrame:
    frame = pd.DataFrame(PROJECTS)
    frame["Sort Date"] = pd.to_datetime(frame["Sort Date"], errors="coerce")
    return frame.sort_values(["Sort Date", "Customer"], na_position="last").reset_index(drop=True)


def render_status_legend() -> None:
    pills = " ".join(
        f"<span class='status-pill' style='background:{color}'>{status}</span>"
        for status, color in STATUS_COLORS.items()
    )
    st.markdown(f"<div class='legend'>{pills}</div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="Upcoming Chain Projects",
        page_icon=":hotel:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
          .block-container {padding-top: 2rem; padding-bottom: 2rem;}
          .source {color: #6b625b; font-size: .9rem;}
          .legend {display: flex; flex-wrap: wrap; gap: .5rem; margin: .25rem 0 1rem;}
          .status-pill {color: white; border-radius: 999px; padding: .28rem .7rem; font-size: .78rem; font-weight: 700;}
          div[data-testid="stMetric"] {background: #fff8f5; border: 1px solid #ecd8cf; border-radius: .65rem; padding: 1rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    frame = project_frame()
    display_frame = frame.drop(columns=["Sort Date"]).copy()
    display_frame["Slack"] = display_frame["Slack"].replace("", None)

    st.title("Upcoming Chain Projects")
    st.markdown(
        "<div class='source'>Source: Upcoming Chain Projects.xlsx - Updated Jul 7, 2026 11:33 AM</div>",
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(2)
    metric_cols[0].metric("Upcoming Chains", len(frame), "5 NAMER / 3 JAPAC")
    metric_cols[1].metric("Hotels in Scope", int(frame["Hotels"].sum()), "112 Minor, 62 Vail, 40 Aramark")

    render_status_legend()

    with st.container(border=True):
        st.subheader("High-Level Project Overview")
        st.dataframe(
            display_frame,
            hide_index=True,
            use_container_width=True,
            height=455,
            column_config={
                "Customer": st.column_config.TextColumn("Customer", width="medium", pinned=True),
                "Region": st.column_config.TextColumn("Region", width="small"),
                "Implementation Lead": st.column_config.TextColumn("Implementation Lead", width="medium"),
                "Hotels": st.column_config.NumberColumn("Hotels", format="%d", width="small"),
                "Channels": st.column_config.TextColumn("Channels", width="large"),
                "Migration Plan": st.column_config.TextColumn("Migration Plan", width="medium"),
                "Slack": st.column_config.LinkColumn("Slack", display_text="Open Slack", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            },
        )


if __name__ == "__main__":
    main()
