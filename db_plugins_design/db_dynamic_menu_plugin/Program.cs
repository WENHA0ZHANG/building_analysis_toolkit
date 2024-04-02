using System;
using System.Collections.Generic;
using System.ComponentModel.Composition;
using System.Windows.Forms;
using System.Text;
using DB.Extensibility.Contracts;
using System.IO;
using DB.Api;

namespace DBDynamicMenuPluginExample
{
    [Export(typeof(IPlugin))]
    public class ExamplePlugin : PluginBase, IPlugin
    {
        class MenuKeys
        {
            public const string Root = "root";
            public const string ReportGeneration = "reportgeneration";
            public const string Visibility = "visibility";
            public const string EnableAll = "enableAll";
            public const string DisableAll = "disableAll";
            public const string VisibleAll = "visibleAll";
            public const string InvisibleAll = "invisibleAll";
        }

        class MenuItem
        {
            public Action Action { get; set; }
            public bool IsEnabled { get; set; }
            public bool IsVisible { get; set; }

            public MenuItem(
                Action action = null,
                bool enabled = true,
                bool visible = true)
            {
                Action = action ?? delegate { };
                IsEnabled = enabled;
                IsVisible = visible;
            }
        }

        private readonly Dictionary<string, MenuItem> mMenuItems = new Dictionary<string, MenuItem>();
        private bool ReportGenerationEnabled = false;

        public override bool HasMenu
        {
            get { return true; }
        }

        public override string MenuLayout
        {
            get
            {
                StringBuilder menu = new StringBuilder();
                menu.AppendFormat("*Plugin,{0}", MenuKeys.Root);
                menu.AppendFormat("*>Report Generation,{0}", MenuKeys.ReportGeneration);
                menu.AppendFormat("*>>Enable,{0}", MenuKeys.EnableAll);
                menu.AppendFormat("*>>Disable,{0}", MenuKeys.DisableAll);
                menu.AppendFormat("*>Visibility,{0}", MenuKeys.Visibility);
                menu.AppendFormat("*>>Make All Visible,{0}", MenuKeys.VisibleAll);
                menu.AppendFormat("*>>Make All Invisible,{0}", MenuKeys.InvisibleAll);
                return menu.ToString();
            }
        }

        public override bool IsMenuItemVisible(string key)
        {
            return mMenuItems[key].IsVisible;
        }

        public override bool IsMenuItemEnabled(string key)
        {
            return mMenuItems[key].IsEnabled;
        }

        public override void OnMenuItemPressed(string key)
        {
            mMenuItems[key].Action();
        }

        public override void Create()
        {
            MessageBox.Show(String.Format("Plugin initialized!", GetType().Namespace));
            mMenuItems.Add(MenuKeys.Root, new MenuItem());
            mMenuItems.Add(MenuKeys.ReportGeneration, new MenuItem());
            mMenuItems.Add(MenuKeys.Visibility, new MenuItem());
            mMenuItems.Add(MenuKeys.EnableAll, new MenuItem(OnEnableAll));
            mMenuItems.Add(MenuKeys.DisableAll, new MenuItem(OnDisableAll));
            mMenuItems.Add(MenuKeys.VisibleAll, new MenuItem(OnVisibleAll));
            mMenuItems.Add(MenuKeys.InvisibleAll, new MenuItem(OnInvisibleAll));
        }

        private void OnEnableAll()
        {
            mMenuItems[MenuKeys.DisableAll].IsEnabled = true;
            mMenuItems[MenuKeys.Visibility].IsEnabled = true;
            ReportGenerationEnabled = true;
        }

        private void OnDisableAll()
        {
            mMenuItems[MenuKeys.DisableAll].IsEnabled = false;
            ReportGenerationEnabled = false;
        }

        private void OnVisibleAll()
        {
            mMenuItems[MenuKeys.InvisibleAll].IsVisible = true;
            mMenuItems[MenuKeys.ReportGeneration].IsVisible = true;
        }

        private void OnInvisibleAll()
        {
            mMenuItems[MenuKeys.InvisibleAll].IsVisible = false;
            mMenuItems[MenuKeys.ReportGeneration].IsVisible = false;
        }

        public override void BeforeEnergyIdfGeneration()
        {
            if (ReportGenerationEnabled)
            {
                StringBuilder report = new StringBuilder();
                Site site = ApiEnvironment.Site;
                report.AppendFormat("Site: {0}\n", site.GetAttribute("Title"));

                foreach (Building building in site.Buildings)
                {
                    PrintBuilding(building, report);
                    foreach (BuildingBlock block in building.BuildingBlocks)
                    {
                        PrintBlock(block, report);
                        foreach (Zone zone in block.Zones)
                        {
                            PrintZone(zone, report);
                            foreach (Surface surface in zone.Surfaces)
                            {
                                PrintSurface(surface, report);
                                foreach (Adjacency adjacency in surface.Adjacencies)
                                {
                                    PrintAdjacency(adjacency, report);
                                    foreach (Opening opening in adjacency.Openings)
                                    {
                                        PrintOpening(opening, report);
                                    }
                                }
                            }
                        }
                    }
                }
                try
                {
                    string energyPlusFolderPath = ApiEnvironment.EnergyPlusFolder;
                    string reportFilePath = Path.Combine(energyPlusFolderPath, "report.txt");
                    File.WriteAllText(reportFilePath, report.ToString());
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error writing file: {ex.Message}");
                }
            }
        }

        private void PrintBuilding(Building building, StringBuilder report)
        {
            report.AppendFormat("+ Building: {0}\n", building.GetAttribute("Title"));
        }

        private void PrintBlock(BuildingBlock block, StringBuilder report)
        {
            report.AppendFormat("  + Block: {0}\n", block.GetAttribute("Title"));
            report.AppendFormat("    - Type: {0}\n", block.Type);
            report.AppendFormat("    - Height: {0}\n", block.Height);
        }

        private void PrintZone(Zone zone, StringBuilder report)
        {
            report.AppendFormat("    + Zone: {0}\n", zone.GetAttribute("Title"));
            report.AppendFormat("      - Area: {0}\n", zone.FloorArea);
            report.AppendFormat("      - Is Merged: {0}\n", zone.IsChildZone);
        }

        private void PrintSurface(Surface surface, StringBuilder report)
        {
            report.AppendFormat("      + Surface: {0}\n", surface.GetAttribute("Title"));
            report.AppendFormat("        - Type: {0}\n", surface.Type);
            report.AppendFormat("        - Area: {0}\n", surface.Area);
            report.AppendFormat("        - Tilt: {0}\n", surface.Tilt);
        }

        private void PrintAdjacency(Adjacency adjacency, StringBuilder report)
        {
            Site site = ApiEnvironment.Site;
            Table table = site.GetTable("Constructions");
            Record record = table.Records.GetRecordFromHandle(adjacency.ConstructionId);
            string ConstructionName = record["Name"];

            report.AppendFormat("        + Adjacency: {0}\n", adjacency.AdjacencyCondition);
            report.AppendFormat("          - Area: {0}\n", adjacency.Area);
            report.AppendFormat("          - Construction name: {0}\n", ConstructionName);
        }

        private void PrintOpening(Opening opening, StringBuilder report)
        {
            Site site = ApiEnvironment.Site;

            if (opening.Type == OpeningType.Window)
            {
                Table table = site.GetTable("Glazing");
                Record record = table.Records.GetRecordFromHandle(opening.ConstructionId);
                string ConstructionName = record["Name"];

                report.AppendFormat("           + Window: {0}\n", "-");
                report.AppendFormat("             - Area: {0}\n", opening.Area);
                report.AppendFormat("             - Glazing name: {0}\n", ConstructionName);
            }
            else if (opening.Type == OpeningType.Door)
            {
                Table table = site.GetTable("Constructions");
                Record record = table.Records.GetRecordFromHandle(opening.ConstructionId);
                string ConstructionName = record["Name"];

                report.AppendFormat("           + Door: {0}\n", "-");
                report.AppendFormat("             - Area: {0}\n", opening.Area);
                report.AppendFormat("             - Construction name: {0}\n", ConstructionName);
            }
            else if (opening.Type == OpeningType.Vent)
            {
                Table table = site.GetTable("Vents");
                int ventId = Int32.Parse(opening.GetAttribute("VentType"));
                Record record = table.Records.GetRecordFromHandle(ventId);
                string ventName = record["Name"];

                report.AppendFormat("           + Vent: {0}\n", "-");
                report.AppendFormat("             - Area: {0}\n", opening.Area);
                report.AppendFormat("             - Vent name: {0}\n", ventName);
            }
            else if (opening.Type == OpeningType.Surface)
            {
                Table table = site.GetTable("Constructions");
                Record record = table.Records.GetRecordFromHandle(opening.ConstructionId);
                string ConstructionName = record["Name"];

                report.AppendFormat("           + Surface: {0}\n", "-");
                report.AppendFormat("             - Area: {0}\n", opening.Area);
                report.AppendFormat("             - Construction name: {0}\n", ConstructionName);
            }
            else if (opening.Type == OpeningType.Hole)
            {
                report.AppendFormat("           + Hole: {0}\n", "-");
                report.AppendFormat("             - Area: {0}\n", opening.Area);
                report.AppendFormat("             - Construction name: {0}\n", "N/A");
            }
        }
    }
}