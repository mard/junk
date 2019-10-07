import {
  IWorkItemChangedArgs,
  IWorkItemFieldChangedArgs,
  IWorkItemFormService,
  IWorkItemLoadedArgs,
  WorkItemTrackingServiceIds
} from "azure-devops-extension-api/WorkItemTracking";
import * as SDK from "azure-devops-extension-sdk";
import { Button } from "azure-devops-ui/Button";
import * as React from "react";
import { showRootComponent } from "./Common";

var output = console.log;

interface WorkItemFormGroupComponentState {
  eventContent: string;
  id: string;
  fields: string;
}

class WorkItemFormGroupComponent extends React.Component<{},  WorkItemFormGroupComponentState> {
  constructor(props: {}) {
    super(props);
    this.state = {
      eventContent: "",
      id: "",
      fields: ""
    };
  }

  public componentDidMount() {
    SDK.init().then(() => {
      this.registerEvents();
    });
  }

  public render(): JSX.Element {
    return (
      <div>
        <Button
          className="sample-work-item-button"
          text="Click me to change title!"
          onClick={() => this.onClickSet()}
        />
        <Button
          className="sample-work-item-button"
          text="Click me to get id!"
          onClick={() => this.onClickGet()}
        />
        <Button
          className="sample-work-item-button"
          text="Get fields"
          onClick={() => this.onClickGetFields()}
        />
        <p>Hi there</p>
        <p><div className="sample-work-item-events">{this.state.eventContent}</div></p>
        <p><div className="sample-work-item-id">{this.state.id}</div></p>
        <p><div className="sample-work-item-id">{this.state.fields}</div></p>
      </div>
    );
  }

  private registerEvents() {
    SDK.register(SDK.getContributionId(), () => {
      return {
        // Called when the active work item is modified
        onFieldChanged: (args: IWorkItemFieldChangedArgs) => {
          this.setState({
            eventContent: `onFieldChanged - ${JSON.stringify(args)}`
          });
          output(JSON.stringify(this.state));
        },

        // Called when a new work item is being loaded in the UI
        onLoaded: (args: IWorkItemLoadedArgs) => {
          this.setState({
            eventContent: `onLoaded - ${JSON.stringify(args)}`
          });
          output(JSON.stringify(this.state));
        },

        // Called when the active work item is being unloaded in the UI
        onUnloaded: (args: IWorkItemChangedArgs) => {
          this.setState({
            eventContent: `onUnloaded - ${JSON.stringify(args)}`
          });
          output(JSON.stringify(this.state));
        },

        // Called after the work item has been saved
        onSaved: (args: IWorkItemChangedArgs) => {
          this.setState({
            eventContent: `onSaved - ${JSON.stringify(args)}`
          });
          this.onClickSet();
          output(JSON.stringify(this.state));
        },

        // Called when the work item is reset to its unmodified state (undo)
        onReset: (args: IWorkItemChangedArgs) => {
          this.setState({
            eventContent: `onReset - ${JSON.stringify(args)}`
          });
          output(JSON.stringify(this.state));
        },

        // Called when the work item has been refreshed from the server
        onRefreshed: (args: IWorkItemChangedArgs) => {
          this.setState({
            eventContent: `onRefreshed - ${JSON.stringify(args)}`
          });
          output(JSON.stringify(this.state));
        }
      };
    });
  }

  private async onClickSet() {
    const workItemFormService = await SDK.getService<IWorkItemFormService>(
      WorkItemTrackingServiceIds.WorkItemFormService
    );
    workItemFormService.setFieldValue(
      "Custom.Codenames",
      `${Math.floor(Math.random() * 100) + 1}`
    );
    workItemFormService.save();
  }

  private async onClickGet() {
    const workItemFormService = await SDK.getService<IWorkItemFormService>(
      WorkItemTrackingServiceIds.WorkItemFormService
    );
    const workItemId = (await workItemFormService.getFieldValue('System.Id')) as string;
    this.setState({id: `id is ${workItemId}`})
    output(JSON.stringify(this.state));
  }

  private async onClickGetFields() {
    const workItemFormService = await SDK.getService<IWorkItemFormService>(
      WorkItemTrackingServiceIds.WorkItemFormService
    );
    const data = (await workItemFormService.getFields());
    this.setState({fields: `Fields are ${JSON.stringify(data)}`})
    output(JSON.stringify(this.state));
  }
}

showRootComponent(<WorkItemFormGroupComponent />);
