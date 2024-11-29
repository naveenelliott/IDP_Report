import streamlit as st
import pandas as pd
from GettingPSDLineupData import getting_PSD_data, getting_PSD_min_data
from streamlit_gsheets import GSheetsConnection

# Setting the title of the PMR App in web browser
st.set_page_config(page_title='Bolts IDP Report App')

st.sidebar.success('Select a page above.')

st.title("Bolts Player Rating App")
st.markdown("Select the team and bolts player to see their performance this season.")

end_df = getting_PSD_data()

end_df = end_df[~end_df['Team Name'].str.contains('NAL', case=False, na=False)].reset_index()

gks = ['Dylan Jacobson', 'Liam Muller', 'Jack Susi', 'Drew Cosby', 'Drew Crosby', 'Milo Ketnouvong', 'Conor Downey', 'Ben Marro', 'Jack Seaborn',
      'Dean Lundqvist', 'Ethan Fine', 'Nate Sykora', 'Casey Powers', 'Aaron Choi', 'Henry Wasserman']

end_df = end_df.loc[~end_df['Player Full Name'].isin(gks)].reset_index()

teams = sorted(list(end_df['Team Name'].unique()))


selected_team = st.session_state.get('selected_team', teams[0])
if selected_team not in teams:
    selected_team = teams[0]  # Default to the first date if not found

selected_team = st.selectbox('Choose the Bolts Team:', teams, index=teams.index(selected_team))
st.session_state['selected_team'] = selected_team

end_df = end_df.loc[end_df['Team Name'] == st.session_state['selected_team']]

players = sorted(list(end_df['Player Full Name'].unique()))

st.session_state['all_players'] = players

selected_player = st.session_state.get('selected_player', players[0])
if selected_player not in players:
    selected_player = players[0]  # Default to the first date if not found

selected_player = st.selectbox('Choose a Bolts Player:', players, index=players.index(selected_player))
st.session_state['selected_player'] = selected_player

conn = st.connection('gsheets', type=GSheetsConnection)

existing_data = conn.read(worksheet='IDP_Plan', ttl=5)
existing_data.dropna(how='all', inplace=True)
existing_data['Bolts Team'] = existing_data['Bolts Team'].fillna('').astype(str)
existing_data['Player Name'] = existing_data['Player Name'].fillna('').astype(str)

coach_notes = ''
focus_spring = ''

updated_df = pd.DataFrame()

index = []

player_exists = (
    existing_data['Bolts Team'].str.contains(selected_team).any() & 
    existing_data['Player Name'].str.contains(selected_player).any()
    )

# Check if the selected match data already exists
if player_exists:
    index = existing_data[
            (existing_data['Bolts Team'] == selected_team) &
            (existing_data['Player Name'] == selected_player)].index

    updated_df = existing_data.copy()

    if not index.empty:
        coach_notes = existing_data.loc[index, "Coach's Summary"].values[0]
        focus_spring = existing_data.loc[index, 'Focus for Spring'].values[0]


# Form to update the DataFrame
with st.form("input_form"):
    coach_notes = st.text_input("Coach's Summary:", value=coach_notes)
    focus_spring = st.text_input('Focus for Spring:', value=focus_spring)
    submit_button = st.form_submit_button(label='Save')

    if submit_button:
        # Ensure all fields are filled
        if not coach_notes or not focus_spring:
            st.warning('Ensure all fields are filled')
            st.stop()
        
        # Update existing data if match data exists
        if player_exists and not index.empty:
            existing_data.loc[index, "Coach's Summary"] = coach_notes
            existing_data.loc[index, 'Focus for Spring'] = focus_spring
            updated_df = existing_data.copy()
        else:
            # Add new data if match data does not exist
            new_data = pd.DataFrame([{
                'Bolts Team': selected_team,
                'Player Name': selected_player, 
                "Coach's Summary": coach_notes,
                'Focus for Spring': focus_spring
            }])
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        
        # Update the Google Sheet
        conn.update(worksheet='IDP_Plan', data=updated_df)
        st.success("Input updated!")
        st.rerun()  # Rerun to refresh the displayed DataFrame

