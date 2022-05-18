local function RadioTest()
    RADIO1 = UNIT:FindByName("RADIO1")
    SCHEDULER:New( nil,
            function()
                SergeyRadio = RADIO1:GetRadio()

                local randomRadio = math.random(1, #KData)
                SergeyRadio:SetFileName(KData[randomRadio].file)
                SergeyRadio:SetFrequency(225)
                SergeyRadio:SetModulation(radio.modulation.AM)
                SergeyRadio:SetSubtitle(KData[randomRadio].title, 5)
                SergeyRadio:SetLoop(false)
                SergeyRadio:SetPower(500)
                SergeyRadio:Broadcast()
            end,{}, 1, 5, 0
    )
end


_SETTINGS:SetPlayerMenuOff()

local MenuTest = MENU_MISSION:New( "TESTS" )
MENU_MISSION_COMMAND:New( "RADIO TEST", MenuTest, RadioTest )




