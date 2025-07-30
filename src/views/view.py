# views/view.py
import flet as ft
import shutil
import os

# --- App Theme & Style (Dark Theme) ---
C_BACKGROUND = "#1A202C"
C_PRIMARY = "#4682A9"
C_SECONDARY = "#749BC2"
C_ACCENT = "#91C8E4"
C_FONT_BODY = "white"
C_CONTAINER = "#2D3748"
FONT_HEADER = "fonts/OskariG2.otf"
FONT_BODY = "fonts/HelveticaBold.ttf"

class View:
    """Defines all Flet UI components for the application."""
    def __init__(self, controller):
        self.controller = controller
        self.page = None
        self.controls = {}
        self.dialog = ft.AlertDialog(modal=True, bgcolor=C_CONTAINER)

    def _setup_page(self):
        """Sets up the page with theme colors, fonts, and the persistent dialog."""
        self.page.bgcolor = C_BACKGROUND
        self.page.fonts = {"Oskari G2": FONT_HEADER, "Helvetica Bold": FONT_BODY}
        self.page.theme = ft.Theme(font_family="Helvetica Bold", text_theme=ft.TextTheme(body_medium=ft.TextStyle(color=C_FONT_BODY)))
        self.page.dialog = self.dialog

    def show_snackbar(self, message, color="red"):
        if not self.page: return
        color_map = {"red": ft.Colors.RED_400, "green": ft.Colors.GREEN_400, "blue": C_PRIMARY, "orange": ft.Colors.ORANGE_400}
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message, font_family="Helvetica Bold"), bgcolor=color_map.get(color, ft.Colors.RED_400))
        self.page.snack_bar.open = True
        self.page.update()

    # --- Dialogs and Overlays ---
    def show_loading_dialog(self, is_loading):
        if is_loading:
            self.dialog.title = ft.Text("Loading...", font_family="Oskari G2", text_align=ft.TextAlign.CENTER, color=C_ACCENT)
            self.dialog.content = ft.Row([ft.ProgressRing(color=C_ACCENT)], alignment=ft.MainAxisAlignment.CENTER)
            self.dialog.actions = []
            self.dialog.open = True
        else:
            self.dialog.open = False
        self.page.update()

    def show_error_dialog(self, message):
        self.dialog.title = ft.Text("Error", font_family="Oskari G2", color=ft.Colors.RED_400)
        self.dialog.content = ft.Text(message)
        self.dialog.actions = [ft.TextButton("OK", on_click=lambda _: self._close_dialog())]
        self.dialog.actions_alignment = ft.MainAxisAlignment.END
        self.dialog.open = True
        self.page.update()

    def show_success_dialog(self, message):
        self.dialog.title = ft.Text("Success!", font_family="Oskari G2", color=ft.Colors.GREEN_400)
        self.dialog.content = ft.Text(message)
        self.dialog.actions = [ft.TextButton("Return to Home", on_click=lambda _: self._close_dialog_and_reset_splash())]
        self.dialog.open = True
        self.page.update()
        
    def show_confirmation_dialog(self, title, message, on_confirm):
        def handle_confirmation(confirmed):
            self._close_dialog()
            if confirmed: on_confirm()
        self.dialog.title = ft.Text(title, font_family="Oskari G2", color=C_ACCENT)
        self.dialog.content = ft.Text(message)
        self.dialog.actions = [ft.ElevatedButton(text="Yes", on_click=lambda _: handle_confirmation(True), bgcolor=C_PRIMARY, color="white"), ft.ElevatedButton(text="No", on_click=lambda _: handle_confirmation(False), bgcolor=C_SECONDARY, color="white")]
        self.dialog.actions_alignment = ft.MainAxisAlignment.END
        self.dialog.open = True
        self.page.update()

    def show_map_dialog(self, map_file):
        # This assumes Flet supports WebView (if not, you can open the file externally)
        webview = ft.WebView(src=map_file, width=800, height=600)
        self.dialog.title = ft.Text("User Location Map")
        self.dialog.content = webview
        self.dialog.actions = [ft.TextButton("Close", on_click=lambda _: self._close_dialog())]
        self.dialog.open = True
        self.page.update()

    def _close_dialog(self):
        self.dialog.open = False
        self.page.update()

    def _close_dialog_and_reset_splash(self):
        self._close_dialog()
        self.controller.reset_splash_view()

    # --- Splash, Login & Register Views ---
    def get_splash_view(self):
        """Builds the initial splash screen with dynamic forms."""
        self._setup_page()

        # --- UI Controls (shared where possible) ---
        self.controls['login_username'] = ft.TextField(label="Username", width=300, border_color=C_SECONDARY)
        self.controls['login_password'] = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, border_color=C_SECONDARY)
        
        # Learner Register
        self.controls['learner_reg_firstname'] = ft.TextField(label="First Name", width=150, border_color=C_SECONDARY)
        self.controls['learner_reg_lastname'] = ft.TextField(label="Last Name", width=150, border_color=C_SECONDARY)
        self.controls['learner_reg_mi'] = ft.TextField(label="M.I.", width=70, border_color=C_SECONDARY)
        self.controls['learner_reg_username'] = ft.TextField(label="Username", width=380, border_color=C_SECONDARY, on_blur=lambda e: self.controller.check_username_availability(e.control.value))
        self.controls['learner_reg_email'] = ft.TextField(label="Email", width=380, border_color=C_SECONDARY)
        self.controls['learner_reg_password'] = ft.TextField(label="Password", password=True, can_reveal_password=True, width=380, border_color=C_SECONDARY)
        self.controls['learner_reg_verify_password'] = ft.TextField(label="Verify Password", password=True, can_reveal_password=True, width=380, border_color=C_SECONDARY)
        self.controls['learner_reg_consent'] = ft.Checkbox(label="I agree to the terms and conditions regarding data privacy and account creation.")

        # Instructor Register
        self.controls['inst_reg_firstname'] = ft.TextField(label="First Name", width=150, border_color=C_SECONDARY)
        self.controls['inst_reg_lastname'] = ft.TextField(label="Last Name", width=150, border_color=C_SECONDARY)
        self.controls['inst_reg_mi'] = ft.TextField(label="M.I.", width=70, border_color=C_SECONDARY)
        self.controls['inst_reg_username'] = ft.TextField(label="Username", width=380, border_color=C_SECONDARY, on_blur=lambda e: self.controller.check_username_availability(e.control.value))
        self.controls['inst_reg_email'] = ft.TextField(label="Email", width=380, border_color=C_SECONDARY)
        self.controls['inst_reg_password'] = ft.TextField(label="Password", password=True, can_reveal_password=True, width=380, border_color=C_SECONDARY)
        self.controls['inst_reg_verify_password'] = ft.TextField(label="Verify Password", password=True, can_reveal_password=True, width=380, border_color=C_SECONDARY)
        self.controls['inst_reg_consent_teach'] = ft.Checkbox(label="I consent to be a responsible instructor and provide a safe learning environment.")
        self.controls['inst_reg_consent_location'] = ft.Checkbox(label="I consent to the use of my location for matchmaking purposes.")
        self.controls['resume_path'] = ft.Text(value="", visible=False)
        self.controls['resume_filename'] = ft.Text("No file selected.")

        def on_resume_picked(e: ft.FilePickerResultEvent):
            if not e.files: return
            source_file = e.files[0].path
            resumes_dir = os.path.join("assets", "resumes")
            os.makedirs(resumes_dir, exist_ok=True)
            unique_filename = f"{int(ft.time.time_ns())}-{os.path.basename(source_file)}"
            destination_file = os.path.join(resumes_dir, unique_filename)
            shutil.copy(source_file, destination_file)
            relative_path = os.path.join("assets", "resumes", unique_filename).replace("\\", "/")
            self.controls['resume_path'].value = relative_path
            self.controls['resume_filename'].value = os.path.basename(source_file)
            self.page.update()

        resume_picker = ft.FilePicker(on_result=on_resume_picked)
        self.page.overlay.append(resume_picker)

        # --- Button Containers ---
        self.controls['initial_buttons'] = ft.Column([
            ft.ElevatedButton("User Login", on_click=lambda _: self._toggle_form('login'), width=300, height=50, bgcolor=C_PRIMARY, color="white"),
            ft.ElevatedButton("Register as Learner", on_click=lambda _: self._toggle_form('learner'), width=300, height=50, bgcolor=C_SECONDARY, color="white"),
            ft.ElevatedButton("Apply as Instructor", on_click=lambda _: self._toggle_form('instructor'), width=300, height=50, bgcolor=C_SECONDARY, color="white"),
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # --- Form Containers (initially hidden) ---
        self.controls['login_form'] = ft.Container(visible=False, content=ft.Column([ft.Text("User Login", font_family="Oskari G2", size=32, color=C_ACCENT), self.controls['login_username'], self.controls['login_password'], ft.ElevatedButton("Login", on_click=lambda _: self.controller.handle_login(self.controls['login_username'].value, self.controls['login_password'].value), width=300, bgcolor=C_PRIMARY, color="white"), ft.TextButton("<- Back", on_click=lambda _: self._toggle_form('initial'))], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        self.controls['learner_register_form'] = ft.Container(visible=False, content=ft.Column([ft.Text("Create Learner Account", font_family="Oskari G2", size=32, color=C_ACCENT), ft.Row([self.controls['learner_reg_firstname'], self.controls['learner_reg_lastname'], self.controls['learner_reg_mi']], alignment=ft.MainAxisAlignment.CENTER), self.controls['learner_reg_username'], self.controls['learner_reg_email'], self.controls['learner_reg_password'], self.controls['learner_reg_verify_password'], ft.Container(self.controls['learner_reg_consent'], alignment=ft.alignment.center), ft.ElevatedButton("Register", on_click=self._handle_learner_register_click, width=300, bgcolor=C_PRIMARY, color="white"), ft.TextButton("Return to Splash Screen", on_click=lambda _: self._toggle_form('initial'))], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        self.controls['instructor_register_form'] = ft.Container(visible=False, content=ft.Column([ft.Text("Apply as Instructor", font_family="Oskari G2", size=32, color=C_ACCENT), ft.Row([self.controls['inst_reg_firstname'], self.controls['inst_reg_lastname'], self.controls['inst_reg_mi']], alignment=ft.MainAxisAlignment.CENTER), self.controls['inst_reg_username'], self.controls['inst_reg_email'], self.controls['inst_reg_password'], self.controls['inst_reg_verify_password'], ft.Row([ft.ElevatedButton("Upload Resume (PDF)", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: resume_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])), self.controls['resume_filename']], alignment=ft.MainAxisAlignment.CENTER), ft.Container(self.controls['inst_reg_consent_teach'], alignment=ft.alignment.center), ft.Container(self.controls['inst_reg_consent_location'], alignment=ft.alignment.center), ft.ElevatedButton("Apply", on_click=self._handle_instructor_register_click, width=300, bgcolor=C_PRIMARY, color="white"), ft.TextButton("Return to Splash Screen", on_click=lambda _: self._toggle_form('initial'))], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER))

        return ft.View("/", [ft.Column([ft.Text("Let's Ingles", font_family="Oskari G2", size=50, color=C_ACCENT), ft.Text("Your Community English Proficiency Program", size=16, color=C_SECONDARY), ft.Container(height=30), ft.Container(padding=40, border_radius=10, bgcolor=C_CONTAINER, content=ft.Column([self.controls['initial_buttons'], self.controls['login_form'], self.controls['learner_register_form'], self.controls['instructor_register_form']]))], horizontal_alignment=ft.CrossAxisAlignment.CENTER)], vertical_alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def _toggle_form(self, form_name):
        self.controls['initial_buttons'].visible = (form_name == 'initial')
        self.controls['login_form'].visible = (form_name == 'login')
        self.controls['learner_register_form'].visible = (form_name == 'learner')
        self.controls['instructor_register_form'].visible = (form_name == 'instructor')
        self.page.update()

    def _validate_and_get_data(self, fields):
        is_valid = True
        for field in fields: field.error_text = None
        for field in fields:
            if not field.value:
                field.error_text = "Required"; is_valid = False
        return is_valid

    def _handle_learner_register_click(self, e):
        fields_to_validate = [self.controls['learner_reg_firstname'], self.controls['learner_reg_lastname'], self.controls['learner_reg_username'], self.controls['learner_reg_email'], self.controls['learner_reg_password'], self.controls['learner_reg_verify_password']]
        is_valid = self._validate_and_get_data(fields_to_validate)
        pwd = self.controls['learner_reg_password']; verify_pwd = self.controls['learner_reg_verify_password']
        if pwd.value != verify_pwd.value:
            verify_pwd.error_text = "Passwords do not match"; is_valid = False
        self.page.update()
        if not is_valid: return
        def on_confirm_action():
            self.controller.handle_register(role='learner', first_name=self.controls['learner_reg_firstname'].value, last_name=self.controls['learner_reg_lastname'].value, middle_initial=self.controls['learner_reg_mi'].value, username=self.controls['learner_reg_username'].value, email=self.controls['learner_reg_email'].value, password=self.controls['learner_reg_password'].value, verify_password=self.controls['learner_reg_verify_password'].value, consent=self.controls['learner_reg_consent'].value)
        self.show_confirmation_dialog("Confirm Registration", "Are you sure you want to create this account?", on_confirm_action)
    
    def _handle_instructor_register_click(self, e):
        fields_to_validate = [self.controls['inst_reg_firstname'], self.controls['inst_reg_lastname'], self.controls['inst_reg_username'], self.controls['inst_reg_email'], self.controls['inst_reg_password'], self.controls['inst_reg_verify_password']]
        is_valid = self._validate_and_get_data(fields_to_validate)
        pwd = self.controls['inst_reg_password']; verify_pwd = self.controls['inst_reg_verify_password']
        if pwd.value != verify_pwd.value:
            verify_pwd.error_text = "Passwords do not match"; is_valid = False
        self.page.update()
        if not is_valid: return
        def on_confirm_action():
            all_consents = self.controls['inst_reg_consent_teach'].value and self.controls['inst_reg_consent_location'].value
            self.controller.handle_register(role='instructor', first_name=self.controls['inst_reg_firstname'].value, last_name=self.controls['inst_reg_lastname'].value, middle_initial=self.controls['inst_reg_mi'].value, username=self.controls['inst_reg_username'].value, email=self.controls['inst_reg_email'].value, password=self.controls['inst_reg_password'].value, verify_password=self.controls['inst_reg_verify_password'].value, consent=all_consents, resume_path=self.controls['resume_path'].value)
        self.show_confirmation_dialog("Confirm Application", "Are you sure you want to apply as an instructor?", on_confirm_action)
    
    # --- DASHBOARD VIEWS ---
    def get_learner_view(self):
        self._setup_page()
        return ft.View("/learner", [self._build_header("Learner Dashboard"), self._build_learner_dashboard_tabs()])

    def get_instructor_view(self):
        self._setup_page()
        return ft.View("/instructor", [self._build_header("Instructor Dashboard"), self._build_instructor_dashboard_tabs()])

    def get_admin_view(self):
        self._setup_page()
        return ft.View("/admin", [self._build_header("Admin Dashboard")])

    def _build_header(self, title):
        return ft.Container(content=ft.Row([ft.Text(title, font_family="Oskari G2", size=28, weight=ft.FontWeight.BOLD, color=C_ACCENT), ft.Row([ft.Text(f"Logged in as: {self.controller.current_user['userName']}"), ft.IconButton(icon=ft.Icons.LOGOUT, on_click=lambda _: self.controller.handle_logout(), tooltip="Logout", icon_color="white")])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER), padding=ft.padding.only(bottom=20))

    def _build_learner_dashboard_tabs(self):
        profile_tab = self._build_profile_tab('learner')
        assignments_tab = self._build_assignments_tab_learner()
        messages_tab = self._build_messages_tab()
        return ft.Tabs(tabs=[profile_tab, assignments_tab, messages_tab], expand=True)

    def _build_instructor_dashboard_tabs(self):
        profile_tab = self._build_profile_tab('instructor')
        assignments_tab = self._build_assignments_tab_instructor()
        messages_tab = self._build_messages_tab()
        return ft.Tabs(tabs=[profile_tab, assignments_tab, messages_tab], expand=True)

    def _build_profile_tab(self, role):
        profile_data_row = self.controller.get_user_profile()
        profile_data = dict(profile_data_row) if profile_data_row else {}
        
        pic_path = profile_data.get('profilePicture') or "assets/placeholder.png"
        profile_image = ft.Image(src=pic_path, width=150, height=150, fit=ft.ImageFit.COVER, border_radius=100)
        
        def on_file_picked(e: ft.FilePickerResultEvent):
            if not e.files: return
            source_file = e.files[0].path
            base_assets_dir = os.path.join(os.getcwd(), "src", "assets")
            os.makedirs(base_assets_dir, exist_ok=True)
            user_assets_dir = os.path.join(base_assets_dir, str(self.controller.current_user['userId']))
            os.makedirs(user_assets_dir, exist_ok=True)
            destination_file = os.path.join(user_assets_dir, os.path.basename(source_file))
            shutil.copy(source_file, destination_file)
            relative_path = os.path.join("assets", str(self.controller.current_user['userId']), os.path.basename(source_file)).replace("\\", "/")
            profile_image.src = relative_path
            self.controls['profile_pic_path'].value = relative_path
            self.page.update()

        file_picker = ft.FilePicker(on_result=on_file_picked)
        self.page.overlay.append(file_picker)
        
        self.controls['profile_pic_path'] = ft.TextField(value=pic_path, visible=False)
        first_name = ft.TextField(label="First Name", value=profile_data.get('firstName', ''), border_color=C_SECONDARY)
        last_name = ft.TextField(label="Last Name", value=profile_data.get('lastName', ''), border_color=C_SECONDARY)
        middle_initial = ft.TextField(label="M.I.", width=70, value=profile_data.get('middleInitial', ''), border_color=C_SECONDARY)
        age = ft.TextField(label="Age", keyboard_type=ft.KeyboardType.NUMBER, value=str(profile_data.get('age', '')))
        education_level = ft.Dropdown(label="Level of Education", value=profile_data.get('educationLevel'), options=[ft.dropdown.Option(text) for text in ["High School", "Undergraduate", "Graduate", "Post-Graduate", "N/A"]], border_color=C_SECONDARY)
        about_me = ft.TextField(label="About Me", multiline=True, max_length=5000, value=profile_data.get('aboutMe', ''), border_color=C_SECONDARY)
        
        role_specific_fields = []
        if role == 'learner':
            school = ft.TextField(label="Current School", value=profile_data.get('school', ''), border_color=C_SECONDARY)
            role_specific_fields.append(school)
        else: # instructor
            occupation = ft.TextField(label="Current Occupation", value=profile_data.get('occupation', ''), border_color=C_SECONDARY)
            specialization = ft.TextField(label="Specializes In", value=profile_data.get('specialization', ''), border_color=C_SECONDARY)
            role_specific_fields.extend([occupation, specialization])

        def save_profile(e):
            data = {"firstName": first_name.value, "lastName": last_name.value, "middleInitial": middle_initial.value, "age": int(age.value) if age.value.isdigit() else None, "educationLevel": education_level.value, "aboutMe": about_me.value, "profilePicture": self.controls['profile_pic_path'].value}
            if role == 'learner':
                data["school"] = role_specific_fields[0].value
            else:
                data["occupation"] = role_specific_fields[0].value
                data["specialization"] = role_specific_fields[1].value
            self.controller.handle_update_profile(data)

        show_map_btn = ft.ElevatedButton(
            "Show My Location on Map",
            on_click=lambda _: self.controller.show_user_location_on_map(
                self.controller.current_user['userLat'],
                self.controller.current_user['userLong']
            ),
            bgcolor=C_PRIMARY, color="white"
        )

        return ft.Tab(text="My Profile", icon=ft.Icons.PERSON, content=ft.ListView(controls=[ft.Row([profile_image, ft.ElevatedButton("Change Picture", icon=ft.Icons.UPLOAD_FILE, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["png", "jpg", "jpeg"]))], alignment=ft.MainAxisAlignment.CENTER), ft.Row([first_name, last_name, middle_initial], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), ft.Row([age, education_level], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), *role_specific_fields, about_me, ft.ElevatedButton("Save Profile", icon=ft.Icons.SAVE, on_click=save_profile, bgcolor=C_PRIMARY, color="white"), show_map_btn], spacing=15, padding=20, expand=True))

    # --- Assignments Tabs ---
    def _build_assignments_tab_learner(self):
        assignments_data = self.controller.get_learner_assignments_with_status()
        
        def on_submit_click(e):
            assignment_id = e.control.data
            self.show_confirmation_dialog("Confirm Submission", "Are you sure you want to mark this assignment as complete?", lambda: self.controller.handle_submit_assignment(assignment_id))

        rows = []
        for assign in assignments_data:
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(assign['title'])),
                ft.DataCell(ft.Text(assign['skillName'])),
                ft.DataCell(ft.Text(assign['instructorName'])),
                ft.DataCell(ft.Text(assign['dueDate'])),
                ft.DataCell(ft.Text(assign['status'], color=ft.Colors.GREEN_400 if assign['status'] == 'Completed' else ft.Colors.YELLOW_400)),
                ft.DataCell(ft.IconButton(icon=ft.Icons.CHECK, icon_color=ft.Colors.GREEN_400, on_click=on_submit_click, data=assign['assignmentID']) if assign['status'] == 'Pending' else ft.Container())
            ]))

        assignments_table = ft.DataTable(columns=[ft.DataColumn(ft.Text(col, font_family="Oskari G2")) for col in ["Title", "Skill", "Instructor", "Due Date", "Status", "Submit"]], rows=rows, expand=True)
        return ft.Tab(text="Assignments", icon=ft.Icons.ASSIGNMENT, content=ft.Container(ft.Column([ft.Text("My Assignments", font_family="Oskari G2", size=22, color=C_ACCENT), assignments_table]), padding=20))

    def _build_assignments_tab_instructor(self):
        def open_create_assignment_dialog(e):
            skill_options = [ft.dropdown.Option(key=skill['skillID'], text=skill['skillName']) for skill in self.controller.get_all_skills()]
            skill_dd = ft.Dropdown(label="Skill", options=skill_options, border_color=C_SECONDARY)
            title_tf = ft.TextField(label="Title", border_color=C_SECONDARY)
            desc_tf = ft.TextField(label="Description", multiline=True, border_color=C_SECONDARY)
            due_date_tf = ft.TextField(label="Due Date (YYYY-MM-DD)", border_color=C_SECONDARY)

            def create_action(e):
                if self.controller.handle_create_assignment(skill_dd.value, title_tf.value, desc_tf.value, due_date_tf.value):
                    self._close_dialog()
                    self.page.go("/instructor")

            self.dialog.title = ft.Text("Create New Assignment", font_family="Oskari G2", color=C_ACCENT)
            self.dialog.content = ft.Column([skill_dd, title_tf, desc_tf, due_date_tf])
            self.dialog.actions = [ft.ElevatedButton("Create", on_click=create_action, bgcolor=C_PRIMARY, color="white"), ft.TextButton("Cancel", on_click=lambda _: self._close_dialog())]
            self.dialog.open = True
            self.page.update()

        create_button = ft.ElevatedButton("Create New Assignment", icon=ft.Icons.ADD, on_click=open_create_assignment_dialog, bgcolor=C_PRIMARY, color="white")
        return ft.Tab(text="Assignments", icon=ft.Icons.ASSIGNMENT, content=ft.Container(ft.Column([create_button]), padding=20))

    # --- Messages Tab ---
    def _build_messages_tab(self):
        partners = self.controller.get_conversation_partners()
        chat_history = ft.ListView(expand=True, auto_scroll=True, spacing=10)
        message_input = ft.TextField(label="Type a message...", expand=True, border_color=C_SECONDARY)
        chat_view = ft.Column([ft.Text("Select a conversation", italic=True)], expand=True)

        def send_message_click(e):
            receiver_id = chat_view.data
            content = message_input.value
            if self.controller.handle_send_message(receiver_id, content):
                chat_history.controls.append(ft.Row([ft.Container(ft.Text(f"Me: {content}"), bgcolor=C_PRIMARY, padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.END))
                message_input.value = ""
                self.page.update()

        def on_partner_click(e):
            partner_id = e.control.data
            conversation = self.controller.get_conversation(partner_id)
            chat_history.controls.clear()
            for msg in conversation:
                is_me = msg['senderID'] == self.controller.current_user['userId']
                chat_history.controls.append(ft.Row([ft.Container(ft.Text(f"{msg['senderName']}: {msg['content']}"), bgcolor=C_PRIMARY if is_me else C_CONTAINER, padding=10, border_radius=10)], alignment=ft.MainAxisAlignment.END if is_me else ft.MainAxisAlignment.START))
            chat_view.data = partner_id
            chat_view.controls[0] = chat_history # Replace placeholder text
            self.page.update()

        partner_list = ft.ListView(controls=[ft.ListTile(title=ft.Text(p['userName']), data=p['userId'], on_click=on_partner_click) for p in partners], expand=True)
        
        chat_view.controls.append(ft.Row([message_input, ft.IconButton(icon=ft.Icons.SEND, on_click=send_message_click, icon_color=C_ACCENT)]))
        
        return ft.Tab(text="Messages", icon=ft.Icons.MESSAGE, content=ft.Row([ft.Container(partner_list, width=250, border=ft.border.only(right=ft.BorderSide(1, C_SECONDARY))), chat_view], expand=True))
