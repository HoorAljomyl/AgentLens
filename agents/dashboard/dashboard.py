import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="AgentLens Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AgentLens Dashboard")
st.caption("AI Agent Evaluation & Debugging Platform")

API_URL = "http://127.0.0.1:8000"


if st.button("Run Evaluation"):
    try:
        response = requests.get(f"{API_URL}/simulate")
        data = response.json()

        results_df = pd.DataFrame(data["results"])

        # =========================
        # Metrics
        # =========================

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Tests",
            data["total_users"],
        )

        col2.metric(
            "Passed",
            data["passed_tests"],
        )

        col3.metric(
            "Failed",
            data["failed_tests"],
        )

        col4.metric(
            "Average Score",
            data["average_score"],
        )

        # =========================
        # Filters
        # =========================

        st.divider()
        st.subheader("Filters")

        filter_col1, filter_col2 = st.columns(2)

        personalities = [
            "All"
        ] + sorted(
            results_df["personality"]
            .dropna()
            .unique()
            .tolist()
        )

        failure_types = [
            "All"
        ] + sorted(
            results_df["failure_type"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_personality = filter_col1.selectbox(
            "Personality",
            personalities,
        )

        selected_failure = filter_col2.selectbox(
            "Failure Type",
            failure_types,
        )

        filtered_df = results_df.copy()

        if selected_personality != "All":
            filtered_df = filtered_df[
                filtered_df["personality"]
                == selected_personality
            ]

        if selected_failure != "All":
            filtered_df = filtered_df[
                filtered_df["failure_type"]
                == selected_failure
            ]

        # =========================
        # Charts
        # =========================

        st.divider()
        st.subheader("Performance Overview")

        chart_data = pd.DataFrame(
            {
                "Status": ["Passed", "Failed"],
                "Count": [
                    data["passed_tests"],
                    data["failed_tests"],
                ],
            }
        )

        pie_fig = px.pie(
            chart_data,
            names="Status",
            values="Count",
            title="Passed vs Failed",
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True,
        )

        if not filtered_df.empty:
            score_fig = px.bar(
                filtered_df,
                x="user",
                y="score",
                title="Scores by User",
                hover_data=[
                    "personality",
                    "message",
                    "failure_type",
                ],
            )

            score_fig.update_yaxes(
                range=[0, 100]
            )

            st.plotly_chart(
                score_fig,
                use_container_width=True,
            )

            failure_data = (
                filtered_df["failure_type"]
                .value_counts()
                .reset_index()
            )

            failure_data.columns = [
                "Failure Type",
                "Count",
            ]

            failure_fig = px.bar(
                failure_data,
                x="Failure Type",
                y="Count",
                title="Failure Types",
            )

            st.plotly_chart(
                failure_fig,
                use_container_width=True,
            )

        else:
            st.warning(
                "No results match the selected filters."
            )

        # =========================
        # Download CSV
        # =========================

        st.divider()
        st.subheader("Export Results")

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="agentlens_results.csv",
            mime="text/csv",
        )

        # =========================
        # Evaluation Results
        # =========================

        st.divider()
        st.subheader("Evaluation Results")

        filtered_results = (
            filtered_df
            .to_dict("records")
        )

        for result in filtered_results:

            status_icon = (
                "✅"
                if result["passed"]
                else "❌"
            )

            with st.expander(
                f"{status_icon} "
                f"{result['user']} — "
                f"{result['personality']}"
            ):

                st.write(
                    "**Message:**",
                    result["message"],
                )

                st.write(
                    "**Agent Response:**",
                    result["response"],
                )

                st.write(
                    "**Score:**",
                    result["score"],
                )

                st.progress(
                    int(result["score"])
                )

                st.write(
                    "**Passed:**",
                    result["passed"],
                )

                st.write(
                    "**Failure Type:**",
                    result["failure_type"],
                )

                st.write(
                    "**Recommendation:**",
                    result["recommendation"],
                )

                st.write(
                    "**LLM Judgment:**",
                    result["llm_judgment"],
                )

                st.markdown("### Trace")

                for step in result["trace"]["steps"]:

                    st.markdown(
                        f"**→ {step['step']}**"
                    )

                    st.json(
                        step["data"]
                    )

    except Exception as error:
        st.error(
            f"Could not connect to AgentLens API: {error}"
        )