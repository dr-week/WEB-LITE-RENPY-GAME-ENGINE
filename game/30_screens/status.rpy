# LOLA - Status Dashboard Screen

screen status():
    tag menu
    $ portfolio = bitcoin_summary()
    $ btc_units_text = "{:.4f}".format(portfolio["units"])
    $ btc_value_text = "{:.2f}".format(portfolio["value"])
    $ job_title_text = current_job["name"] if current_job else "Seeking part-time work"

    use game_menu(_("Maya's Status Dashboard"), scroll="viewport", spacing=18):
        vbox:
            xfill True
            spacing 20

            hbox:
                xfill True
                spacing 18
                frame:
                    style "status_summary_card"
                    hbox:
                        spacing 12
                        add Transform("images/ui/icons/calendar.png", xysize=(36, 36)) yalign 0.5
                        vbox:
                            spacing 4
                            text "Schedule & Location" style "status_card_title"
                            text "Day [current_day] • [time_slot.title()]" style "status_value"
                            text "[get_location_name(current_location)]" style "status_value_small"
                frame:
                    style "status_summary_card"
                    hbox:
                        spacing 12
                        add Transform("images/ui/icons/cash.png", xysize=(36, 36)) yalign 0.5
                        vbox:
                            spacing 4
                            text "Wallet & Portfolio" style "status_card_title"
                            text "$[money] [currency]" style "status_value"
                            text "BTC: [btc_units_text] ($[btc_value_text])" style "status_value_small"
                frame:
                    style "status_summary_card"
                    hbox:
                        spacing 12
                        add Transform("images/ui/icons/trophy.png", xysize=(36, 36)) yalign 0.5
                        vbox:
                            spacing 4
                            text "Career & Standing" style "status_card_title"
                            text "[employment_state.title()] • Rep [reputation]" style "status_value"
                            text "[job_title_text]" style "status_value_small"

            hbox:
                xfill True
                spacing 22
                frame:
                    style "status_column_card"
                    vbox:
                        xfill True
                        spacing 14
                        text "Wellbeing & Study" style "status_card_title"
                        for ic, stat_label, stat_val in [("energy", "Energy", energy), ("education", "Education", education_progress), ("stress", "Stress", stress)]:
                            vbox:
                                xfill True
                                spacing 6
                                hbox:
                                    xfill True
                                    hbox:
                                        spacing 8
                                        add Transform("images/ui/icons/%s.png" % ic, xysize=(20, 20)) yalign 0.5
                                        text stat_label style "status_label"
                                    text "[stat_val]/100" style "status_stat_num"
                                bar value StaticValue(stat_val, 100) style "status_bar"
                frame:
                    style "status_column_card"
                    vbox:
                        xfill True
                        spacing 14
                        text "Skills & Presence" style "status_card_title"
                        for ic, stat_label, stat_val in [("intelligence", "Intelligence", intelligence), ("appeal", "Appeal", appeal), ("target", "Confidence", confidence)]:
                            vbox:
                                xfill True
                                spacing 6
                                hbox:
                                    xfill True
                                    hbox:
                                        spacing 8
                                        add Transform("images/ui/icons/%s.png" % ic, xysize=(20, 20)) yalign 0.5
                                        text stat_label style "status_label"
                                    text "[stat_val]/100" style "status_stat_num"
                                bar value StaticValue(stat_val, 100) style "status_bar"

            frame:
                xfill True
                background Solid("#202436")
                padding (22, 16)
                vbox:
                    spacing 6
                    text "Practical Skills & State of Mind" style "status_card_title"
                    text "Mood: [emotional_state.title()]   •   Learning: [learning]   •   Communication: [communication]   •   Work Skill: [work_skill]   •   Finance: [financial_literacy]" style "status_value_small"
